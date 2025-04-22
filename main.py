# Main file for the diffenent steps of the pipeline in extending mintaka with additional languages

# Pipeline overview:
# 1. Extract List of english questions from the mintaka dataset
# 2. Translate the questions to the target language
    # 2.1. Pause and validate sample translations
# 3. If relevant query wikidata for correct label/labels in the targeted language for the answer entities. 
    # 3.1. Pause and validate sample labels
# 4. Update the mintaka json with newly translated questions and relevant labels. 

from Utils.extract_questions import extract_questions
from Utils.generate_questions_txt_file import generate_questions_txt_file
from Utils.extract_answer_entities import extract_answer_entities
from Utils.generate_random_translation_sampling_sheet import generate_random_translation_sampling_sheet
from Services.wikidata import get_wikidata_labels
from Services.file_service import write_json, open_json
from Utils.extend_mintaka_json import extend_mintaka_json
from Utils.generate_answer_label_sheet import generate_answer_label_sheet
from Translation.google_integration import google_translate_line_by_line
from Translation.deepl_integration import deepl_translate_large_text_file
import os
data_paths = {
    'dev': './data/mintaka_dev.json',
}
# this object should be created on the fly when the pipeline is done
txt_files = {
    'dev' : {
        "English": "./outputs/questions_txt_files/dev_questions.txt",
        "Translations": {
            "da": "./outputs/translations/deepl/dev_questions_da.txt",
            "bn": "./outputs/translations/google/dev_questions_bn_linebyline.txt",
            "fi": "./outputs/translations/fi/dev_questions_fi.txt"
        }  
    },
    'test' : {
        "English": "./outputs/questions_txt_files/test_questions.txt",
        "Translations": {
            "da": "./outputs/translations/deepl/test_questions_da.txt",
            "bn": "./outputs/translations/google/test_questions_bn_linebyline.txt"
        }
    },
    'train' : {
        "English": "./outputs/questions_txt_files/train_questions.txt",
        "Translations": {
            "da": "./outputs/translations/deepl/train_questions_da.txt",
            "bn": "./outputs/translations/google/train_questions_bn_linebyline.txt"
        }
    }
}


translate = False
samples = 100 # amount of translated samples extracted to excel sheet for validation
extend_mintaka = True

output_paths = {
    'dev': './data/id2question_dev.json',
    'test': './data/id2question_test.json',
    'train': './data/id2question_train.json',
}
def run_pipeline(data_paths, output_paths, lang_codes = ["fi"]):
    if translate:
        translation_functions = {
            "bn": google_translate_line_by_line,
            "da": deepl_translate_large_text_file,
            "fi": deepl_translate_large_text_file,
        }
        for key, path in data_paths.items():
            json_map = extract_questions(path, output_paths[key])
            questions_path = f'./outputs/questions_txt_files/{key}_questions.txt'
            for lang in lang_codes:
                if lang in translation_functions:
                    dest_path = f'./outputs/translations/{lang}/{key}_questions_{lang}.txt'
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)  # Ensure directory exists
                    translation_functions[lang](questions_path, dest_path, lang)
                    txt_files[key]["Translations"][lang] = dest_path
    if(samples > 0):
        generate_random_translation_sampling_sheet(txt_files, samples, lang_codes, "dev")
                   
                
    # pause and validate the translations
        
            
    
    # first step with translation done, now we will find wikidata labels for the answer entities
    if extend_mintaka:
        for key, d_path in data_paths.items():
            dataset_name = os.path.basename(d_path).replace(".json","")
            answer_entities = extract_answer_entities(d_path)
            write_json(answer_entities, f'./outputs/answer_entities_maps/{dataset_name}_answer_entities.json')
            answer_labels = get_wikidata_labels(answer_entities, f'./outputs/answer_labels/{dataset_name}_answer_labels.json')
            write_json(answer_labels, f'./outputs/answer_labels/{dataset_name}_answer_labels.json')
            translated_files = txt_files[key]["Translations"]
            extend_mintaka_json(d_path, answer_labels, translated_files)
            answer_labels = open_json(f'./outputs/answer_labels/{dataset_name}_answer_labels.json')
            generate_answer_label_sheet(answer_labels, lang_codes, dataset_name)
            
    

run_pipeline(data_paths, output_paths)
