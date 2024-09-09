import os
import json
import re
import logging
from dataclasses import dataclass
from typing import List, Dict
from dotenv import load_dotenv
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
from openai import OpenAIError  # Correct way to import OpenAIError


load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Requirement:
    """Represents a single requirement derived from the style guide."""
    name: str
    description: str
    applicable_sections: List[str]

@dataclass
class StyleGuide:
    """Represents the entire style guide with its requirements."""
    requirements: List[Requirement]

@dataclass
class Article:
    """Represents a Wikipedia article."""
    title: str
    sections: Dict[str, str]  # section name: content

@dataclass
class EvaluatedSection:
    """Represents an evaluated section from an article."""
    section: str
    score: float
    feedback: str

class LanguageModel:
    """Wrapper for interacting with the OpenAI API."""

    def __init__(self, model_identifier: str = "gpt-4o-mini"):
        self.model_identifier = model_identifier

    def prompt(self, text: str) -> str:
        try:
            response = client.chat.completions.create(  # For completion models
                model=self.model_identifier,
                messages=[{"role": "user", "content": text}],
                response_format= { "type":"json_object" }
            )

            return response.choices[0].message.content
        except OpenAIError as e:  # Corrected to use the right exception class
            logger.error(f"OpenAI API error: {e}")
            raise

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
        # logger.info("Raw response: %s", response)

        try:
            cleaned_response = response.strip().strip('```json').strip('```')
            return json.loads(cleaned_response)
        except json.JSONDecodeError as e:
            logger.error("Failed to parse JSON: %s", e)
            logger.error("Cleaned response: %s", cleaned_response)
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
        # logger.info("Raw response: %s", response)

        try:
            cleaned_response = response.strip().strip('```json').strip('```')
            refined_data = json.loads(cleaned_response)
            rules = refined_data.get('rules', [])
        
            return [Requirement(**req) for req in rules]
        
        except json.JSONDecodeError as e:
            logger.error("Failed to parse JSON: %s", e)
            logger.error("Cleaned response: %s", cleaned_response)
            raise

class Section:
    """Represents a section of the article."""
    def __init__(self, title, content=None, subsections=None, images=None, links=None):
        self.title = title
        self.content = content if content else []
        self.subsections = subsections if subsections else []
        self.images = images if images else []
        self.links = links if links else []

    def add_content(self, line):
        self.content.append(line)

    def add_image(self, image):
        self.images.append(image)

    def add_link(self, link):
        self.links.append(link)

    def add_subsection(self, section):
        self.subsections.append(section)

    def __repr__(self):
        return f"Section(title={self.title}, content={self.content}, images={self.images}, links={self.links}, subsections={self.subsections})"


class ArticleParser:
    """Parses Wikipedia articles into a structured format."""

    @staticmethod
    def parse(article_text: str) -> Article:
        lines = article_text.split('\n')
        title = lines[0].strip()  # First line is the title
        sections = {}
        current_section = Section("Introduction")

        section_stack = [current_section]
        sections[current_section.title] = current_section

        # Regex patterns for structure
        section_pattern = re.compile(r'^## (.+)')
        subsection_pattern = re.compile(r'^### (.+)')
        image_pattern = re.compile(r'!\[.*\]\((.*)\)')
        link_pattern = re.compile(r'\[(.*?)\]\((.*?)\)')

        for line in lines[1:]:
            line = line.strip()

            # Section Header
            if section_pattern.match(line):
                section_title = section_pattern.match(line).group(1)
                current_section = Section(section_title)
                sections[current_section.title] = current_section
            
            # Subsection Header
            elif subsection_pattern.match(line):
                subsection_title = subsection_pattern.match(line).group(1)
                subsection = Section(subsection_title)
                current_section.add_subsection(subsection)
            
            # Images
            elif image_pattern.match(line):
                image_link = image_pattern.match(line).group(1)
                current_section.add_image(image_link)

            # Links
            elif link_pattern.search(line):
                links = link_pattern.findall(line)
                for text, url in links:
                    current_section.add_link((text, url))
                current_section.add_content(line)  # Add content containing the link

            # Regular content
            else:
                if line:
                    current_section.add_content(line)

        # Prepare final structure
        section_content = {section.title: '\n'.join(section.content) for section in sections.values()}
        return Article(title=title, sections=section_content)


class ArticleEvaluator:
    """Evaluates an article against the extracted requirements."""

    def __init__(self, llm, requirements: List[Requirement]):
        self.llm = llm
        self.requirements = requirements

    def evaluate(self, article: Article) -> List[EvaluatedSection]:
        evaluated_sections = []
        for section, content in article.sections.items():
            applicable_reqs = [r for r in self.requirements if section in r.applicable_sections]
            score, feedback = self._evaluate_section(section, content, applicable_reqs)
            evaluated_sections.append(EvaluatedSection(section, score, feedback))
        return evaluated_sections

    def _evaluate_section(self, section_name: str, content: str, requirements: List[Requirement]) -> (float, str):
        print(f"Evaluating section: {section_name}")
        prompt = f"""
        Evaluate the section: "{section_name}"
        Content: "{content}"
        Against these requirements:
        {json.dumps([req.__dict__ for req in requirements])}

        Provide:
        1. A score from 0 to 1 (1 being perfect adherence)
        2. Feedback explaining the score

        Return as JSON: {{"score": float, "notes": "string"}}
        """
        response = self.llm.prompt(prompt)
        logger.info("Raw response: %s", response)

        try:
            result = json.loads(response)
            return result['score'], result['notes']
        except json.JSONDecodeError as e:
            logger.error("Failed to parse JSON: %s", e)
            raise

class Omnipedia:
    """Main class orchestrating the Omnipedia system."""

    def __init__(self, style_guide_path: str):
        self.llm = LanguageModel()
        self.style_guide = StyleGuideProcessor(style_guide_path).process()
        self.evaluator = ArticleEvaluator(self.llm, self.style_guide.requirements)

    def evaluate_article(self, article_path: str) -> List[EvaluatedSection]:
        with open(article_path, 'r') as file:
            article_text = file.read()
        article = ArticleParser.parse(article_text)
        return self.evaluator.evaluate(article)

    def generate_report(self, evaluated_sections: List[EvaluatedSection]) -> str:
        prompt = f"""
        Generate a human-readable report from these evaluated sections:
        {json.dumps([es.__dict__ for es in evaluated_sections])}

        The report should include:
        1. An overall summary of the article's adherence to the style guide
        2. Section-by-section breakdown of strengths and weaknesses
        3. Specific examples of good and bad sections
        4. Suggestions for improvement

        Format the report with markdown for readability.
        """
        response = self.llm.prompt(prompt)
        # logger.info("Raw response: %s", response)
        return response

    def save_evaluated_sections(self, evaluated_sections: List[EvaluatedSection], filename: str):
        """Save evaluated sections to a JSON file."""
        data = [
            {
                "section": es.section,
                "score": es.score,
                "feedback": es.feedback
            }
            for es in evaluated_sections
        ]
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Evaluated sections saved to {filename}")

def main():
    try:
        omnipedia = Omnipedia("data/style.txt")
        evaluated_sections = omnipedia.evaluate_article("data/article.md")
        omnipedia.save_evaluated_sections(evaluated_sections, "evaluated_sections.json")

        # Uncomment the following lines to generate and print a report
        # report = omnipedia.generate_report(evaluated_sections)
        # print(report)
    except Exception as e:
        logger.error("An error occurred: %s", e)

if __name__ == "__main__":
    main()

