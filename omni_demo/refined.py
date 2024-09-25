import os
import json
import re
import logging
from dataclasses import dataclass
from typing import List, Dict
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError
import networkx as nx
from scipy.sparse import lil_matrix

# Load environment variables
load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@dataclass
class Requirement:
    name: str
    description: str
    applicable_sections: List[str]

@dataclass
class StyleGuide:
    requirements: List[Requirement]

@dataclass
class ArticleNode:
    location: str
    content: str
    category: str

@dataclass
class EvaluatedSection:
    section: str
    score: float
    feedback: str
    adherent_requirements: List[str]

@dataclass
class TaxonomyRule:
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
    def __init__(self, model_identifier: str = "gpt-4o-mini"):
        self.model_identifier = model_identifier

    def prompt(self, text: str) -> str:
        try:
            response = client.chat.completions.create(
                model=self.model_identifier,
                messages=[{"role": "user", "content": text}],
                response_format={"type": "json_object"}
            )
            return response.choices[0].message.content
        except OpenAIError as e:
            logger.error(f"OpenAI API error: {e}")
            raise

class ArticleGraph:
    """Directed Acyclic Graph to represent the hierarchy of article components."""
    
    def __init__(self):
        self.graph = nx.DiGraph()
        self.node_id_to_index = {}  # Map node_id to integer index
        self.current_index = 0      # Keep track of the current index

    def add_node(self, node_id: str, content: str, category: str):
        """Add a node representing a location (section/paragraph/sentence) to the graph."""
        self.graph.add_node(node_id, data=ArticleNode(location=node_id, content=content, category=category))
        
        # Assign a unique integer index for this node
        self.node_id_to_index[node_id] = self.current_index
        self.current_index += 1

    def add_edge(self, parent_id: str, child_id: str):
        """Add a directed edge between two nodes (parent-child relationship)."""
        self.graph.add_edge(parent_id, child_id)

    def get_node(self, node_id: str) -> ArticleNode:
        """Retrieve a node (article location) by its ID."""
        return self.graph.nodes[node_id]['data']

    def get_children(self, node_id: str):
        """Get all children of a node (subsections)."""
        return list(self.graph.successors(node_id))

    def get_node_index(self, node_id: str) -> int:
        """Retrieve the integer index of a node based on its node_id."""
        return self.node_id_to_index[node_id]

class TaxonomyClassifier:
    """Classifies sections of a Wikipedia article based on predefined taxonomy rules."""
    @staticmethod
    def classify(section_title: str) -> str:
        """Classify a section based on its title using taxonomy rules."""
        for rule in TAXONOMY_RULES:
            if re.search(rule.section_pattern, section_title, re.IGNORECASE):
                return rule.category
        return "Unknown"

class RequirementMapper:
    """Sparse matrix for requirement mapping"""
    
    def __init__(self, num_locations: int, num_requirements: int):
        self.sparse_matrix = lil_matrix((num_locations, num_requirements), dtype=bool)
        self.requirements = []

    def add_requirements(self, requirements: List[Requirement]):
        """Add the requirements to the system."""
        self.requirements = requirements

    def assign_requirement(self, location_idx: int, requirement_idx: int):
        """Assign a requirement to a specific location."""
        self.sparse_matrix[location_idx, requirement_idx] = True

    def get_requirements_for_location(self, location_idx: int) -> List[Requirement]:
        """Get all requirements for a specific location."""
        return [self.requirements[i] for i in self.sparse_matrix.rows[location_idx]]

class ArticleParser:
    """Parses Wikipedia articles into structured format and builds the graph."""
    
    def __init__(self):
        self.article_graph = ArticleGraph()

    def parse(self, article_text: str):
        """Parse the article into sections and subsections using a graph structure."""
        sections = article_text.split('## ')  # This assumes the article uses '##' for sections.
        
        root_id = 'root'
        self.article_graph.add_node(root_id, '', 'root')

        for i, section in enumerate(sections):
            section_lines = section.strip().split('\n')
            
            # First line should be the section title, others are content
            if section_lines:
                section_title = section_lines[0].strip()  # Section header
                section_content = '\n'.join(section_lines[1:]).strip()  # Remaining lines as content
                
                section_id = f'section_{i}'
                
                # Classify the section and add it to the graph
                section_category = TaxonomyClassifier.classify(section_title)
                self.article_graph.add_node(section_id, section_content, section_category)
                
                # Add edge from root to this section (can change to parent-child relations if needed)
                self.article_graph.add_edge(root_id, section_id)

        return self.article_graph

class ArticleEvaluator:
    """Evaluates the sections of the article based on the assigned requirements."""
    
    def __init__(self, llm, requirements: List[Requirement]):
        self.llm = llm
        self.requirements = requirements

    def evaluate(self, article_graph: ArticleGraph, requirement_mapper: RequirementMapper) -> List[EvaluatedSection]:
        evaluated_sections = []
        for node_id in article_graph.graph.nodes:
            node = article_graph.get_node(node_id)
            
            # Get the integer index for the node (location)
            location_idx = article_graph.get_node_index(node_id)
            
            # Retrieve applicable requirements based on the integer index
            applicable_requirements = requirement_mapper.get_requirements_for_location(location_idx)
            
            content = node.content
            score, feedback, adherent_reqs = self._evaluate_section(node.location, content, applicable_requirements)
            evaluated_sections.append(EvaluatedSection(section=node.location, score=score, feedback=feedback, adherent_requirements=adherent_reqs))
        return evaluated_sections


    def _evaluate_section(self, section_name: str, content: str, requirements: List[Requirement]) -> (float, str, List[str]):
        prompt = f"""
        Evaluate the section: "{section_name}"
        Content: "{content}"
        Against these requirements:
        {json.dumps([req.__dict__ for req in requirements])}

        Provide:
        1. A score from 0 to 1 (1 being perfect adherence)
        2. Feedback explaining the score
        3. List of adherent requirements

        Return as JSON: {{"score": float, "notes": "string", "adherent_requirements": ["string"]}}
        """
        response = self.llm.prompt(prompt)
        try:
            result = json.loads(response)
            return result['score'], result['notes'], result['adherent_requirements']
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {e}")
            raise

class Omnipedia:
    """Orchestrates the Omnipedia system."""
    
    def __init__(self, style_guide_path: str):
        self.llm = LanguageModel()
        self.style_guide = StyleGuideProcessor(style_guide_path).process()
        self.evaluator = ArticleEvaluator(self.llm, self.style_guide.requirements)
        self.requirement_mapper = RequirementMapper(num_locations=10, num_requirements=len(self.style_guide.requirements))

    def evaluate_article(self, article_path: str) -> List[EvaluatedSection]:
        parser = ArticleParser()
        with open(article_path, 'r') as file:
            article_text = file.read()
        article_graph = parser.parse(article_text)
        
        assigner = RequirementAssigner(self.requirement_mapper)
        assigner.assign(article_graph, self.style_guide.requirements)
        
        return self.evaluator.evaluate(article_graph, self.requirement_mapper)

    def save_evaluated_sections(self, evaluated_sections: List[EvaluatedSection], filename: str):
        """Save evaluated sections to a JSON file."""
        data = [
            {
                "section": es.section,
                "score": es.score,
                "feedback": es.feedback,
                "adherent_requirements": es.adherent_requirements
            }
            for es in evaluated_sections
        ]
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"Evaluated sections saved to {filename}")

class RequirementAssigner:
    """Assigns requirements to article locations based on section type and hierarchical structure."""
    
    def __init__(self, requirement_mapper: RequirementMapper):
        self.requirement_mapper = requirement_mapper

    def assign(self, article_graph: ArticleGraph, requirements: List[Requirement]):
        """Assign relevant requirements to each section or paragraph in the article, considering hierarchy."""
        
        # Iterate through all nodes (sections) in the article graph
        for node_id in article_graph.graph.nodes:
            node = article_graph.get_node(node_id)
            logging.debug(f"Assigning requirements for node: {node.location}, category: {node.category}")
            
            # Find the integer index of the node
            location_idx = article_graph.get_node_index(node_id)

            # Assign requirements directly based on node category
            applicable_requirements = self._find_applicable_requirements(node.category, requirements)

            # Map applicable requirements to this node (using integer index)
            for req in applicable_requirements:
                self.requirement_mapper.assign_requirement(location_idx, requirements.index(req))

            # Propagate global or parent-relevant requirements to child nodes
            if self._is_parent_relevant(node.category):
                self._assign_to_children(node_id, article_graph, applicable_requirements)

    def _find_applicable_requirements(self, category: str, requirements: List[Requirement]) -> List[Requirement]:
        """Find applicable requirements for a given category of a section."""
        applicable = [req for req in requirements if category in req.applicable_sections]
        logging.debug(f"Found {len(applicable)} applicable requirements for category '{category}'")
        return applicable
    
    def _is_parent_relevant(self, category: str) -> bool:
        """Determine if a requirement should be propagated to subsections based on the section type."""
        # Example: "Body" sections should propagate requirements to subsections
        return category in ["Body", "Introduction", "Metadata"]

    def _assign_to_children(self, parent_id: str, article_graph: ArticleGraph, parent_requirements: List[Requirement]):
        """Recursively assign applicable parent requirements to child sections."""
        
        # Get the children of the current node (parent)
        for child_id in article_graph.get_children(parent_id):
            location_idx = article_graph.get_node_index(child_id)
            child_node = article_graph.get_node(child_id)
            logging.debug(f"Propagating requirements from parent {parent_id} to child {child_node.location}")
            
            # Propagate parent requirements to the child (using integer index)
            for req in parent_requirements:
                self.requirement_mapper.assign_requirement(location_idx, self.requirement_mapper.requirements.index(req))
            
            # Recursively apply to child nodes
            self._assign_to_children(child_id, article_graph, parent_requirements)

class StyleGuideProcessor:
    """Processes the style guide: reads, parses, and refines requirements."""
    
    def __init__(self, style_guide_path: str):
        self.style_guide_path = style_guide_path
        self.llm = LanguageModel()

    def process(self) -> StyleGuide:
        with open(self.style_guide_path, 'r') as file:
            guide_text = file.read()
        initial_requirements = self._extract_initial_requirements(guide_text)
        refined_requirements = self._refine_requirements(initial_requirements)
        return StyleGuide(requirements=refined_requirements)

    def _extract_initial_requirements(self, guide_text: str) -> List[dict]:
        prompt = f"""
        Analyze this style guide and extract actionable writing rules:
        {guide_text}

        For each rule, provide:
        - Name: A brief title
        - Description: Detailed explanation
        - Applicable sections: List of article parts this applies to

        Return ONLY the rules in this JSON format without any additional text or formatting:
        [
            {{
                "name": "Rule Title",
                "description": "Rule details",
                "applicable_sections": ["Section1", "Section2"]
            }},
            ...
        ]
        """
        response = self.llm.prompt(prompt)
        try:
            cleaned_response = response.strip().strip('```json').strip('```')
            return json.loads(cleaned_response)
        except json.JSONDecodeError as e:
            logger.error("Failed to parse JSON: %s", e)
            raise


    def _refine_requirements(self, initial_requirements: List[dict]) -> List[Requirement]:
        prompt = f"""
        Given these initial style guide requirements:
        {json.dumps(initial_requirements)}

        Refine and clarify these requirements. For each, provide:
        - A concise name
        - A detailed description of how to apply it
        - Specific sections it applies to

        Return ONLY the result in the same JSON format as the input, without any additional text or formatting.
        """
        response = self.llm.prompt(prompt)
        logging.debug(f"Raw LLM response: {response}")
        
        try:
            cleaned_response = response.strip().strip('```json').strip('```')
            logging.debug(f"Cleaned response: {cleaned_response}")
            
            refined_data = json.loads(cleaned_response)
            logging.debug(f"Parsed JSON: {refined_data}")
            
            if isinstance(refined_data, list):
                return [Requirement(
                    name=req.get('name', ''),
                    description=req.get('description', ''),
                    applicable_sections=req.get('applicable_sections', [])
                ) for req in refined_data]
            elif isinstance(refined_data, dict):
                # Handle case where a single requirement is returned
                return [Requirement(
                    name=refined_data.get('name', ''),
                    description=refined_data.get('description', ''),
                    applicable_sections=refined_data.get('applicable_sections', [])
                )]
            else:
                raise ValueError(f"Unexpected data type: {type(refined_data)}")
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse JSON: {e}")
            logging.error(f"Invalid JSON: {cleaned_response}")
            raise
        except Exception as e:
            logging.error(f"Error processing requirements: {e}")
            logging.error(f"Problematic data: {cleaned_response}")
            raise

def main():
    try:
        style = "/Users/sayertindall/Documents/GitHub/block.science/omnipedia/wiki-demo/pipeline/data/style2.txt"
        article = "/Users/sayertindall/Documents/GitHub/block.science/omnipedia/wiki-demo/pipeline/data/article2.md"
        
        # Create an instance of ArticleParser
        parser = ArticleParser()
        
        # Read the article content
        with open(article, 'r') as file:
            article_text = file.read()
        
        # Parse the article
        article_graph = parser.parse(article_text)
        
        # Print the parsed article structure
        print("Parsed Article Structure:")
        for node_id in article_graph.graph.nodes:
            node = article_graph.get_node(node_id)
            print(f"Node ID: {node_id}")
            print(f"Location: {node.location}")
            print(f"Category: {node.category}")
            print(f"Content: {node.content[:100]}...")  # Print first 100 characters of content
            print("---")
            
        # omnipedia = Omnipedia(style)
        # evaluated_sections = omnipedia.evaluate_article(article)
        # omnipedia.save_evaluated_sections(evaluated_sections, "evaluated_sections2.json")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
