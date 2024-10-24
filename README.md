# Aggregated Results for Omnipedia

This guide provides comprehensive instructions on how to query the MongoDB database for the Omnipedia project. The database houses collections of documents related to various genes, representing the aggregated results of evaluation processes conducted by Omnipedia and WikiCrow.

Omnipedia leverages advanced language models to transform Wikipedia's Manual of Style into machine-executable requirements. These requirements are then used to systematically assess and grade article sections, ensuring adherence to established guidelines. This framework guarantees detailed applicability, content mapping, and scoring, enhancing the quality and consistency of both user-submitted and AI-generated articles.

## Overview

**Omnipedia** is a research initiative focused on improving Wikipedia articles by automating the evaluation process. By converting natural language style guides into structured, machine-readable requirements, Omnipedia enables efficient and consistent assessment of article content. The project manages two types of articles:

1. **User-Submitted Articles**: Traditional wiki articles created and edited by users.
2. **AI-Generated Articles (Storm/WikiCrow)**: Articles automatically generated based on scientific literature and evaluated for quality and citation accuracy.

## Evaluation Process

The evaluation process in Omnipedia systematically assesses article sections against a predefined set of requirements derived from the style guide. Each section is graded based on its adherence to these guidelines, ensuring comprehensive and objective evaluations.

### Key Aspects of the Evaluation Process

1. **Applicability Assessment**:

   - Each section is evaluated to determine which requirements are relevant.
   - Only applicable requirements are graded based on the section’s purpose.

2. **Content Mapping**:

   - Requirements are mapped to specific content within the section.
   - Evaluators check for missing, incomplete, or overlapping content to ensure all relevant areas are covered.

3. **Grading and Scoring**:

   - Applicable requirements are scored on a scale from 0 to 1, representing degrees of adherence:
     - **0.0**: No adherence
     - **0.25**: Minimal adherence
     - **0.5**: Partial adherence
     - **0.75**: Strong adherence
     - **1.0**: Full adherence
   - Scores are supported by evidence (examples from the content) and reasoning (justifications for the score).

4. **Confidence Rating**:

   - Evaluators assign a confidence level (0 to 1) indicating their certainty that the content meets the requirement.

5. **Overlaps**:

   - The evaluator checks for overlaps between sections and content (e.g., between an infobox and text) to determine if repetition is justified or redundant.

6. **Documentation**:
   - Detailed meta-notes capture additional observations or potential improvements, ensuring transparency and thoroughness in the evaluation process.

## Requirements Extraction

The extraction process involves transforming the [Manual of Style](<https://en.wikipedia.org/wiki/Wikipedia:WikiProject_Molecular_Biology/Style_guide_(gene_and_protein_articles)>) into structured, machine-readable requirements that guide the evaluation of articles.

### Key Aspects of Requirements Extraction

1. **Thorough Review**:

   - The style guide is carefully reviewed to identify all relevant guidelines.
   - Prescriptive language such as "must," "should," and "avoid" is flagged to capture all rules and recommendations.

2. **Organizing Sections and Subsections**:

   - The style guide is broken down into sections and subsections to organize the extracted requirements into logical categories, such as "Content," "Formatting," and "Language Usage."

3. **Extracting Prescriptive Guidelines**:

   - Each section's prescriptive statements are identified and documented, forming the core requirements for articles to meet the expected standards.

4. **Detailed Documentation of Each Requirement**:

   - Each requirement is assigned a unique identifier (e.g., "R1") and categorized based on its type, such as "Content" or "Formatting."
   - The exact wording from the style guide is included as a reference.

5. **Classification**:

   - Requirements are classified into levels of importance:
     - **Imperative Standards**: Non-negotiable rules.
     - **Best Practices**: Strong recommendations.
     - **Flexible Guidelines**: Optional, context-dependent rules.
     - **Contextual Considerations**: Requirements applying only in specific situations.

6. **Mapping Requirements**:

   - Each requirement is mapped to specific sections of an article (e.g., lead section, content section), with notes on when it should be applied.

7. **Grouping Requirements**:

   - The requirements are grouped into relevant categories such as "Content," "Formatting," and "Citations" to streamline their application during article reviews.

8. **Structured JSON Format**:
   - The final output is a structured JSON file, organizing each requirement under its relevant group with fields like:
     - **ID**: Unique identifier (e.g., "R1").
     - **Description**: Summary of the requirement.
     - **Reference**: Exact quote from the style guide.
     - **Category**: Classification by type (e.g., "Content," "Formatting").
     - **Where**: Specifies where in the article the requirement applies.
     - **When**: Details when the requirement is applicable.

## Database Information

### Connection Details

To connect to the MongoDB database, use the following **read-only** connection string:

```plaintext
mongodb+srv://omnipedia:omnipedia@omnipedia.y9tx7.mongodb.net/?retryWrites=true&w=majority&appName=Omnipedia
```

### Structure

The database is organized into collections, each corresponding to a specific gene and source. The collections are named as follows:

_Note: This is just the original results of analysis; more will be added._

- `adcyap1_wikipedia`
- `adcyap1_wikicrow`
- `abcc11_wikipedia`
- `abc11_wikicrow`
- `agk_wikipedia`
- `agk_wikicrow`
- `atf1_wikipedia`
- `atf1_wikicrow`

#### Document Structure

Each document within these collections follows a JSON structure, encompassing various aspects of the article and its evaluation.

Documents in the Wikipedia collections include:

- **`title`**:
  - The title of the article.
- **`content`**:
  - The main content of the article.
- **`hierarchy`**:
  - The hierarchical structure of the article, e.g., `Introduction > References > Citations`.
- **`feedback`**:
  - A nested object containing evaluation categories such as:
    - `Citations`
    - `Formatting`
    - `Content`
    - etc.

##### Feedback Object

Each section of an article is evaluated against specific requirements. The feedback object captures detailed evaluations for each requirement across multiple categories. Here’s an example structure for one section:

```json
{
  "Content": [
    {
      "title": "Introduction",
      "requirement_evaluations": [
        {
          "requirement_id": "R1",
          "applicable": true,
          "applicability_reasoning": "Applicable because the lead section should define the scope of the article.",
          "score": 1.0,
          "confidence": 0.95,
          "evidence": "The lead starts with a clear definition of the AGK gene and its protein product.",
          "reasoning": "The section fully meets the requirement by providing a comprehensive definition at the beginning.",
          "overlap_notes": "No significant overlaps detected."
        },
        {
          "requirement_id": "R2",
          "applicable": true,
          "applicability_reasoning": "Applicable for gene/protein articles with human orthologs in the lead section.",
          "score": 0.75,
          "confidence": 0.85,
          "evidence": "The lead mentions the gene and protein but could more clearly specify the relationship.",
          "reasoning": "Adheres to the requirement but can improve by explicitly clarifying the gene-protein encoding relationship.",
          "overlap_notes": "No significant overlaps detected."
        }
      ],
      "meta_notes": "The section is overall well-structured with comprehensive references and neutral tone. Improvement can be made by clarifying gene-protein relationships and expanding on function details."
    }
  ],
  "Language Usage": [
    {
      "title": "Introduction",
      "requirement_evaluations": [
        {
          "requirement_id": "R1",
          "applicable": true,
          "applicability_reasoning": "Applicable since gene abbreviations are mentioned and need to adhere to HUGO Gene Nomenclature Committee guidelines.",
          "score": 0.75,
          "confidence": 0.9,
          "evidence": "Gene abbreviation 'AGK' is present but not italicized.",
          "reasoning": "The section partially adheres to the requirement as 'AGK' is correctly used, but it does not appear in italic.",
          "overlap_notes": "No overlap with other sections detected."
        }
      ],
      "meta_notes": "The section is informative, using correct capitalization for gene names but misses italicization for gene abbreviations."
    }
  ]
}
```

Each category, such as `Content`, `Language Usage`, `Images and Diagrams`, and `Citations`, has its own evaluations based on specific requirements. These evaluations provide a detailed analysis of how well the article adheres to the style guide.

## Results of Extraction and Evaluation

The collections in the Omnipedia database are the aggregated results of data extraction and evaluation processes conducted by both Omnipedia and WikiCrow:

- **Omnipedia**: Utilizes a language model pipeline to transform style guides into context-sensitive requirements for article review. The system evaluates and annotates each sentence with potential improvements, supporting high-throughput drafts that may need extensive work.

- **WikiCrow**: Automates the synthesis of Wikipedia-style summaries for technical topics from scientific literature. WikiCrow is designed to evaluate articles for citation accuracy and content quality, focusing on creating high-quality articles with citations based on full-text scientific papers.

The data reflects the combined efforts of these systems to provide a curated and evaluated body of scientific content, particularly focused on genes. WikiCrow-generated articles typically exhibit more consistent citation usage compared to human-authored content, though occasional inaccuracies are expected to decrease as models improve.

## Querying the Database

To query the database, you can use the `find` method from the PyMongo library. Below is a Python example of how to query a collection:

```python
from pymongo import MongoClient

# Connect to the MongoDB client
client = MongoClient("mongodb+srv://omnipedia:omnipedia@omnipedia.y9tx7.mongodb.net/?retryWrites=true&w=majority&appName=Omnipedia")
db = client['omnipedia']

def query_collection(collection_name, query={}):
    collection = db[collection_name]
    results = collection.find(query)
    for document in results:
        print(document)

# Example query
query_collection('adcyap1_wikipedia')
```

## Links to Articles

For further reading and exploration, here are links to the articles related to each gene:

- **ADCYAP1**:

  - [Wikipedia](https://en.wikipedia.org/wiki/Pituitary_adenylate_cyclase-activating_peptide1)
  - [WikiCrow](https://wikicrow.ai/ADCYAP1)

- **AGK**:

  - [Wikipedia](<https://en.wikipedia.org/wiki/AGK_(gene)>)
  - [WikiCrow](https://wikicrow.org/AGK)

- **ATF1**:

  - [Wikipedia](https://en.wikipedia.org/wiki/ATF1)
  - [WikiCrow](https://wikicrow.ai/ATF1)

- **ABCC11**:
  - [Wikipedia](https://en.wikipedia.org/wiki/ABCC11)
  - [WikiCrow](https://wikicrow.ai/ABCC11)

## Limitations

- **Style Guide Variability**: Currently tailored to the Wikipedia Manual of Style; adapting to other style guides may require adjustments.
- **AI Evaluation Accuracy**: While robust, AI-generated evaluations may still have instances of misinterpretation or inaccuracies requiring human oversight.
- **Scalability Constraints**: Handling extremely large datasets or highly complex articles may impact performance and require optimization.
- **Dependency on LLM Quality**: Effectiveness heavily depends on the underlying LLM's capabilities and training data.

## Contact and Support

For questions, support, or collaboration inquiries, please reach out to us at:

- **Email**: [sayer@block.science](mailto:sayer@block.science)
