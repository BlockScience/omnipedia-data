import pandas as pd
from dataclasses import dataclass
import re
from typing import List, Type
from os import environ
import requests

@dataclass
class GradeLog:
    TA: str
    Student: str
    Prompt: str
    Response: str
    Notes: str
    Grade: int

class Exam:
    def __init__(self, questions: List[str], question_guidelines: List[str], exam_guidelines: List[str], schema: GradeLog):
        assert issubclass(schema, GradeLog), "Provided schema must be a subclass of Schema or Schema itself."

        self.questions = questions
        self.question_guidelines = question_guidelines
        self.exam_guidelines = exam_guidelines
        self.schema = GradeLog
    
    def summarize_exam(self):
        print("Exam Guidelines:")
        for guideline in self.exam_guidelines:
            print(f"\t{guideline}")
        print("Questions:")
        for i, question in enumerate(self.questions):
            print(f"\t{i+1}. {question}")
            print(f"\t\t{self.question_guidelines[i]}")

class Llm:
    def __init__(self, model_identifier: str = "gpt-4-1106-preview", 
                 url: str = "https://api.openai.com/v1/chat/completions", 
                 role: str = "user",
                 auth: dict = {"Authorization": f"Bearer {environ.get('OPENAI_API_KEY')}"}):
        
        self.model_identifier = model_identifier
        self.url = url
        self.role = role
        self.auth = auth

    @property
    def model_identifier(self):
        return self._model_identifier

    @model_identifier.setter
    def model_identifier(self, value):
        self._model_identifier = value

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, value):
        self._role = value

    @property
    def auth(self):
        return self._auth

    @auth.setter
    def auth(self, value):
        self._auth = value
        
    def prompt(self, text: str) -> str:
        req = {
            "model": self.model_identifier,
            "messages": [
                {"role": self.role, "content": text}
            ]
        }
        response = requests.post(self.url, json=req, headers=self.auth)
        raw = response.json()
        try:
            return f"{response.json()['choices'][0]['message']['content']}"
        except:
            return raw

    def prompt_sequence(self, prompts: List[str]) -> List[str]:
        conversation_history = []
        responses = []

        for prompt in prompts:
            full_prompt = " ".join(conversation_history + [prompt])
            req = {
                "model": self.model_identifier,
                "messages": [{"role": self.role, "content": full_prompt}]
            }
            response = requests.post(self.url, json=req, headers=self.auth)
            raw = response.json()

            try:
                content = raw['choices'][0]['message']['content']
                responses.append(content)
                conversation_history.append(prompt)
                conversation_history.append(content)
            except:
                responses.append(raw)

        return responses

class LLMTest:
    def __init__(self, student_llm: Llm, ta_llm: Llm, exam: Exam):
        self.student_llm = student_llm
        self.ta_llm = ta_llm
        self.exam = exam

    def test(self) -> List[Type[GradeLog]]:
        student_responses = self.student_llm.prompt_sequence(self.exam.questions)
        graded_responses = self.ta_llm.prompt_sequence(self.format_grading_prompt_sequence(student_responses))
        standardized_responses = [self.process_ta_response(self.exam.questions[i], student_responses[i], graded_responses[i+1]) for i in range(len(self.exam.questions))]

        return standardized_responses

    def format_grading_prompt_sequence(self, responses: str) -> str:
        assert(len(self.exam.questions) == len(responses))
        context_str = """You are grading an exam. For each of the follow question:response pairs please provide a grade and notes for the student.
         the grade and the notes for every question should evaluated according to the following guidelines:"""
        context_str += "\n".join(self.exam.exam_guidelines) + "\n As the TA, the professor will be evaluating your evaluations as part of your teaching practicum; your PhD candidacy depends on this. Are you ready to begin?"

        def format_grading_prompt(question: str, response: str, guideline: str) -> str:
            prompt_str = "Question: " + question + "\n received the following response: " + response + "\n Please provide a grade and notes for the student, according to the following guidelines: " + guideline
            return prompt_str
        
        sequence = [context_str] + [format_grading_prompt(self.exam.questions[i], responses[i], self.exam.question_guidelines[i]) for i in range(len(self.exam.questions))]
        return sequence

    def process_ta_response(self, question, student_response, ta_response: str) -> Type[GradeLog]:
        def process_string(input_str: str):
            pattern = r"Grade: (\d+)"
            match = re.search(pattern, input_str)

            if match:
                grade = int(match.group(1))
                notes = input_str.replace(match.group(0), '').strip()
                return notes, grade
            else:
                return input_str, None
        
        notes, grade = process_string(ta_response)
        return GradeLog(TA=self.ta_llm.model_identifier,
                        Student=self.student_llm.model_identifier,
                        Prompt=question,
                        Response=student_response, 
                        Notes=notes, 
                        Grade=grade)

# Load the dataframes from the CSV files
rdf = pd.read_csv("evaluators/requirements_data/section_level_requirements.csv")
stdf = pd.read_csv("evaluators/requirements_data/section_types.csv")
rbsdf = pd.read_csv("evaluators/requirements_data/requirements_by_section_type.csv")

# Example LLM interaction
eval_llm = Llm(model_identifier="gpt-4o")
eval_llm.prompt("poke, please reply")
