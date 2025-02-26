# Main file for the diffenent steps of the pipeline in extending mintaka with additional languages

# Pipeline overview:
# 1. Extract List of english questions from the mintaka dataset
# 2. Translate the questions to the target language
    # 2.1. Pause and validate sample translations
# 3. If relevant query wikidata for correct label/labels in the targeted language for the answer entities. 
    # 3.1. Pause and validate sample labels
# 4. Update the mintaka json with newly translated questions and relevant labels. 

from Utils.extract_questions import extract_questions
from Utils.generate_translation_file import generate_translation_file
data_paths = {
    'train': './data/mintaka_train.json',
    'dev': './data/mintaka_dev.json',
    'test': './data/mintaka_test.json'
}

output_paths = {
    'train': './data/id2question_train.json',
    'dev': './data/id2question_dev.json',
    'test': './data/id2question_test.json'
}
def process_datasets(data_paths, output_paths):
    for key in data_paths:
        print(f"Extracting questions from {key} dataset")
        json_map = extract_questions(data_paths[key], output_paths[key])
        generate_translation_file(json_map, f'./data/{key}_questions.txt')

process_datasets(data_paths, output_paths)
    