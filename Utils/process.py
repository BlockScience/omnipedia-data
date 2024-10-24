import os
import json

def load_and_organize_json_data(json_dir):
    all_json_data = {}
    json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]

    for file in json_files:
        with open(os.path.join(json_dir, file), 'r') as f:
            file_data = json.load(f)
            category, section_title = file[:-5].rsplit('_', 1)
            
            if section_title not in all_json_data:
                all_json_data[section_title] = {}
            
            if category not in all_json_data[section_title]:
                all_json_data[section_title][category] = []

            all_json_data[section_title][category].extend(file_data.get('sections', []))

    return all_json_data

def remove_non_applicable_entries(data):
    for section in data.get("sections", []):
        for _, feedback_list in section.get("feedback", {}).items():
            for feedback in feedback_list:
                feedback["requirement_evaluations"] = [
                    evaluation for evaluation in feedback.get("requirement_evaluations", [])
                    if evaluation.get("applicable") is not False
                ]

def aggregate_json_data(json_dir, article_path, output_file_path):
    all_json_data = load_and_organize_json_data(json_dir)

    with open(article_path, 'r') as a:
        article = json.load(a)

    for article_section in article:
        section_title = article_section['title']
        if section_title in all_json_data:
            article_section['feedback'] = all_json_data[section_title]
        else:
            article_section['feedback'] = {}

    output_json = {"sections": article}
    remove_non_applicable_entries(output_json)

    output_json_str = json.dumps(output_json['sections'], indent=2)

    with open(output_file_path, 'w') as output_file:
        output_file.write(output_json_str)

    print(f"Combined JSON data has been saved to {output_file_path}")

def process_protein(protein):
    json_dir = f'Data/{protein}/wikicrow/results'
    article_path = f'Data/{protein}/wikicrow_article.json'
    output_file_path = f'Documents/{protein}-wikicrow.json'
    aggregate_json_data(json_dir, article_path, output_file_path)

    json_dir = f'Data/{protein}/wikipedia/results'
    article_path = f'Data/{protein}/wikipedia_article.json'
    output_file_path = f'Documents/{protein}-wikipedia.json'
    aggregate_json_data(json_dir, article_path, output_file_path)
    

process_protein('ANLN')