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
from Utils.extract_answer_entities import extract_answer_entities
from Utils.random_translation_sampling import random_translation_sampling
data_paths = {
    'dev': './data/mintaka_dev.json',
}
# this object should be created on the fly when the pipeline is done
txt_files = {
    "English": "../data/dev_questions.txt",
    "Translations": {
        "Danish": "../Translation/dev_questions_da.txt",
    }
}


translate = False
samples = 0 # amount of translated samples extracted to excel sheet for validation

output_paths = {
    'dev': './data/id2question_dev.json',
}
def run_pipeline(data_paths, output_paths):
    for key, path in data_paths.items():
        if translate:
            json_map = extract_questions(path, output_paths[key])
            generate_translation_file(json_map, f'./data/{key}_questions.txt')    
    # Example usage
    if(samples > 0):
        random_translation_sampling(txt_files, samples)
    
    extract_answer_entities(path)

run_pipeline(data_paths, output_paths)
    