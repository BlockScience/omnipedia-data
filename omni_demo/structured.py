import os
import json
import re
import logging
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import litellm
from litellm import completion
import asyncio
import instructor
from instructor import OpenAISchema
import traceback

import wikitextparser as wtp
import networkx as nx
from scipy.sparse import lil_matrix

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
os.environ['LITELLM_LOG'] = 'DEBUG'

client = instructor.from_litellm(completion)

# Pydantic models
class Requirement(BaseModel):
    name: str
    description: str
    applicable_sections: List[str]

class StyleGuide(BaseModel):
    requirements: List[Requirement]

class ArticleNode(BaseModel):
    location: str
    content: str
    category: str

class EvaluatedSection(BaseModel):
    section: str
    score: float
    feedback: str
    adherent_requirements: List[str]
    templates: List[str] = Field(default_factory=list)
    wikilinks: List[str] = Field(default_factory=list)
    external_links: List[str] = Field(default_factory=list)
    list_items: List[str] = Field(default_factory=list)

class TaxonomyRule(BaseModel):
    section_pattern: str
    category: str

# Predefined taxonomy rules
TAXONOMY_RULES = [
    TaxonomyRule(section_pattern="Introduction|Lead", category="Introduction"),
    TaxonomyRule(section_pattern="History", category="Body"),
    TaxonomyRule(section_pattern="Content", category="Body"),
    TaxonomyRule(section_pattern="References|External links|Further reading", category="Metadata"),
    TaxonomyRule(section_pattern="Infobox", category="Infoboxes"),
]

class LanguageModel:
    def __init__(self, model_identifier: str = "gpt-3.5-turbo"):
        self.model_identifier = model_identifier

    async def prompt(self, text: str, response_model):
        try:
            return await client.chat.completions.create(
                model=self.model_identifier,
                messages=[{"role": "user", "content": text}],
                response_model=response_model,
                max_tokens=1000  # Adjust as needed
            )
        except Exception as e:
            logger.error(f"Language model API error: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise

class ArticleGraph:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.node_id_to_index = {}
        self.current_index = 0

    def add_node(self, node_id: str, content: str, category: str):
        self.graph.add_node(node_id, data=ArticleNode(location=node_id, content=content, category=category))
        self.node_id_to_index[node_id] = self.current_index
        self.current_index += 1

    def add_edge(self, parent_id: str, child_id: str):
        self.graph.add_edge(parent_id, child_id)

    def get_node(self, node_id: str) -> ArticleNode:
        return self.graph.nodes[node_id]['data']

    def get_children(self, node_id: str):
        return list(self.graph.successors(node_id))

    def get_node_index(self, node_id: str) -> int:
        return self.node_id_to_index[node_id]

class TaxonomyClassifier:
    @staticmethod
    def classify(section_title: str) -> str:
        for rule in TAXONOMY_RULES:
            if re.search(rule.section_pattern, section_title, re.IGNORECASE):
                return rule.category
        return "Unknown"

class RequirementMapper:
    def __init__(self, num_locations: int, num_requirements: int):
        self.sparse_matrix = lil_matrix((num_locations, num_requirements), dtype=bool)
        self.requirements = []

    def add_requirements(self, requirements: List[Requirement]):
        self.requirements = requirements

    def assign_requirement(self, location_idx: int, requirement_idx: int):
        self.sparse_matrix[location_idx, requirement_idx] = True

    def get_requirements_for_location(self, location_idx: int) -> List[Requirement]:
        return [self.requirements[i] for i in self.sparse_matrix.rows[location_idx]]

class ArticleParser:
    def __init__(self):
        self.article_graph = ArticleGraph()

    async def parse(self, article_text: str):
        try:
            parsed_wikitext = wtp.parse(article_text)
            
            root_id = 'root'
            self.article_graph.add_node(root_id, '', 'root')

            for i, section in enumerate(parsed_wikitext.sections):
                section_id = f'section_{i}'
                section_title = section.title.strip() if section.title else f"Untitled Section {i}"
                section_content = section.contents.strip()
                section_category = TaxonomyClassifier.classify(section_title)
                
                self.article_graph.add_node(section_id, section_content, section_category)
                self.article_graph.add_edge(root_id, section_id)

                # Parse subsections if any
                for j, subsection in enumerate(section.get_sections(level=section.level + 1)):
                    subsection_id = f'section_{i}_{j}'
                    subsection_title = subsection.title.strip() if subsection.title else f"Untitled Subsection {j}"
                    subsection_content = subsection.contents.strip()
                    subsection_category = TaxonomyClassifier.classify(subsection_title)
                    
                    self.article_graph.add_node(subsection_id, subsection_content, subsection_category)
                    self.article_graph.add_edge(section_id, subsection_id)

            return self.article_graph
        except Exception as e:
            logger.error(f"Error parsing article: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise

    @staticmethod
    def extract_templates(parsed_wikitext):
        return [template.name.strip() for template in parsed_wikitext.templates]

    @staticmethod
    def extract_wikilinks(parsed_wikitext):
        return [wikilink.title for wikilink in parsed_wikitext.wikilinks]

    @staticmethod
    def extract_external_links(parsed_wikitext):
        return [link.url for link in parsed_wikitext.external_links]

    @staticmethod
    def extract_lists(parsed_wikitext):
        return [list_item for wikilist in parsed_wikitext.get_lists() for list_item in wikilist.items]

class ArticleEvaluator:
    def __init__(self, llm: LanguageModel, requirements: List[Requirement]):
        self.llm = llm
        self.requirements = requirements

    async def evaluate(self, article_graph: ArticleGraph, requirement_mapper: RequirementMapper) -> List[EvaluatedSection]:
        try:
            sections_to_evaluate = []
            for node_id in article_graph.graph.nodes:
                if node_id != 'root':
                    node = article_graph.get_node(node_id)
                    location_idx = article_graph.get_node_index(node_id)
                    applicable_requirements = requirement_mapper.get_requirements_for_location(location_idx)
                    sections_to_evaluate.append({
                        "section_id": node_id,
                        "location": node.location,
                        "content": node.content,
                        "requirements": [req.dict() for req in applicable_requirements]
                    })

            prompt = f"""
            Evaluate the following article sections against their respective requirements:

            {json.dumps(sections_to_evaluate, indent=2)}

            For each section, provide:
            1. A score from 0 to 1 (1 being perfect adherence)
            2. Feedback explaining the score
            3. List of adherent requirements

            Return the results as a list of EvaluatedSection objects.
            """

            class EvaluatedArticle(BaseModel):
                evaluated_sections: List[EvaluatedSection]

            result = await self.llm.prompt(prompt, EvaluatedArticle)

            for evaluated_section in result.evaluated_sections:
                section_wikitext = wtp.parse(article_graph.get_node(evaluated_section.section).content)
                evaluated_section.templates = ArticleParser.extract_templates(section_wikitext)
                evaluated_section.wikilinks = ArticleParser.extract_wikilinks(section_wikitext)
                evaluated_section.external_links = ArticleParser.extract_external_links(section_wikitext)
                evaluated_section.list_items = ArticleParser.extract_lists(section_wikitext)

            return result.evaluated_sections
        except Exception as e:
            logger.error(f"Error evaluating article: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise

class Omnipedia:
    def __init__(self, style_guide_path: str):
        self.llm = LanguageModel()
        self.style_guide_processor = StyleGuideProcessor(style_guide_path)
        self.style_guide = None
        self.evaluator = None
        self.requirement_mapper = None

    async def initialize(self):
        try:
            self.style_guide = await self.style_guide_processor.process()
            self.evaluator = ArticleEvaluator(self.llm, self.style_guide.requirements)
            self.requirement_mapper = RequirementMapper(num_locations=100, num_requirements=len(self.style_guide.requirements))
            self.requirement_mapper.add_requirements(self.style_guide.requirements)
        except Exception as e:
            logger.error(f"Error initializing Omnipedia: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise

    async def evaluate_article(self, article_path: str) -> List[EvaluatedSection]:
        try:
            parser = ArticleParser()
            with open(article_path, 'r') as file:
                article_text = file.read()
            article_graph = await parser.parse(article_text)
            
            assigner = RequirementAssigner(self.requirement_mapper)
            await assigner.assign(article_graph, self.style_guide.requirements)
            
            return await self.evaluator.evaluate(article_graph, self.requirement_mapper)
        except Exception as e:
            logger.error(f"Error evaluating article: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise

    async def save_evaluated_sections(self, evaluated_sections: List[EvaluatedSection], filename: str):
        try:
            data = [es.dict() for es in evaluated_sections]
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"Evaluated sections saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving evaluated sections: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise

class RequirementAssigner:
    def __init__(self, requirement_mapper: RequirementMapper):
        self.requirement_mapper = requirement_mapper

    async def assign(self, article_graph: ArticleGraph, requirements: List[Requirement]):
        for node_id in article_graph.graph.nodes:
            node = article_graph.get_node(node_id)
            location_idx = article_graph.get_node_index(node_id)
            applicable_requirements = self._find_applicable_requirements(node.category, requirements)

            for req in applicable_requirements:
                self.requirement_mapper.assign_requirement(location_idx, requirements.index(req))

            if self._is_parent_relevant(node.category):
                await self._assign_to_children(node_id, article_graph, applicable_requirements)

    def _find_applicable_requirements(self, category: str, requirements: List[Requirement]) -> List[Requirement]:
        return [req for req in requirements if category in req.applicable_sections]

    def _is_parent_relevant(self, category: str) -> bool:
        return category in ["Body", "Introduction", "Metadata"]

    async def _assign_to_children(self, parent_id: str, article_graph: ArticleGraph, parent_requirements: List[Requirement]):
        for child_id in article_graph.get_children(parent_id):
            location_idx = article_graph.get_node_index(child_id)
            for req in parent_requirements:
                self.requirement_mapper.assign_requirement(location_idx, self.requirement_mapper.requirements.index(req))
            await self._assign_to_children(child_id, article_graph, parent_requirements)

class StyleGuideProcessor:
    def __init__(self, style_guide_path: str):
        self.style_guide_path = style_guide_path
        self.llm = LanguageModel()

    async def process(self) -> StyleGuide:
        try:
            with open(self.style_guide_path, 'r') as file:
                guide_text = file.read()
            requirements = await self._extract_requirements(guide_text)
            return StyleGuide(requirements=requirements)
        except Exception as e:
            logger.error(f"Error processing style guide: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise

    async def _extract_requirements(self, guide_text: str) -> List[Requirement]:
        try:
            prompt = f"""
            Analyze this style guide and extract actionable writing rules:
            {guide_text}

            For each rule, provide:
            - Name: A brief title
            - Description: Detailed explanation
            - Applicable sections: List of article parts this applies to
            """
            return await self.llm.prompt(prompt, List[Requirement])
        except Exception as e:
            logger.error(f"Error extracting requirements: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise

async def main():
    try:
        style_guide_path = "/Users/sayertindall/Documents/GitHub/block.science/omnipedia/wiki-demo/omni_demo/data/style.txt"
        article_path = "/Users/sayertindall/Documents/GitHub/block.science/omnipedia/wiki-demo/omni_demo/data/article.txt"
        
        omnipedia = Omnipedia(style_guide_path)
        await omnipedia.initialize()
        
        evaluated_sections = await omnipedia.evaluate_article(article_path)
        await omnipedia.save_evaluated_sections(evaluated_sections, "evaluated_sections.json")
        
        print("Evaluation complete. Results saved to evaluated_sections.json")
    except Exception as e:
        logger.error(f"An error occurred in main: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    asyncio.run(main())