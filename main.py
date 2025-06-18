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
from shared_utils.file_service import write_json, open_json
from Utils.extend_mintaka_json import extend_mintaka_json
from Utils.generate_answer_label_sheet import generate_answer_label_sheet
from Translation.google_integration import google_translate_line_by_line
from Translation.deepl_integration import deepl_translate_large_text_file
import os
import time

base_dir = os.path.abspath(os.path.dirname(__file__))  # Get the base directory of the script

data_paths = {
    'dev': './data/mintaka_dev.json',
}

txt_files_path = os.path.join(base_dir, "outputs/txt_files.json") 

# Load txt_files from JSON or initialize it if the file doesn't exist
if os.path.exists(txt_files_path):
    txt_files = open_json(txt_files_path)
else:
    txt_files = {}

translate = True
samples = 100 # amount of translated samples extracted to excel sheet for validation
extend_mintaka = True

def run_pipeline(data_paths, lang_codes = ["fi"]):
    if translate:
        translation_functions = {
            "bn": google_translate_line_by_line,
            "da": deepl_translate_large_text_file,
            "fi": deepl_translate_large_text_file,
            "de": deepl_translate_large_text_file,
        }
        for key, path in data_paths.items():
            questions_path = f'./outputs/questions_txt_files/{key}_questions.txt'
            for lang in lang_codes:
                if lang in translation_functions:
                    print(f"Translating {key}_2 questions to {lang}...")
                    dest_path = f'./outputs/translations/{lang}/{key}_questions_{lang}.txt'
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)  # Ensure directory exists
                    translation_functions[lang](questions_path, dest_path, lang)
                    txt_files[key]["Translations"][lang] = dest_path
                    print(f"Translation to {lang} completed and saved to {dest_path}")
                    write_json(txt_files, txt_files_path)  # Update JSON file after adding new translations
                    print(f"Updated txt_files.json with {lang} translations for {key}.")
            if(samples > 0):
                sampling_path = f"./outputs/sampling/sampled_translations_{lang_codes[0]}_{key}.xlsx"
                txt_data_object = txt_files[key]
                print(f"Generating random translation sampling sheet for {key}...")
                generate_random_translation_sampling_sheet(txt_data_object, samples, lang_codes, sampling_path)
        print("Translation pipeline completed. Proceeding with finding wikidata labels...")
        time.sleep(3)  # Pause for 3 seconds before proceeding to the next step

    # first step with translation done, now we will find wikidata labels for the answer entities
    if extend_mintaka:
        for key, d_path in data_paths.items():
            dataset_name = os.path.basename(d_path).replace(".json","")
            print(f"Extracting answer entities from {key} dataset...")
            answer_entities = extract_answer_entities(d_path)
            write_json(answer_entities, f'./outputs/answer_entities_maps/{dataset_name}_answer_entities.json')
            print(f"Answer entities extracted and saved to {dataset_name}_answer_entities.json")
            print(f"Finding wikidata labels for answer entities in {key} dataset... in languages {lang_codes}")
            answer_labels = get_wikidata_labels(answer_entities, f'./outputs/answer_labels/{dataset_name}_answer_labels.json', lang_codes)
            write_json(answer_labels, f'./outputs/answer_labels/{dataset_name}_answer_labels.json')
            print(f"Wikidata labels for answer entities saved to {dataset_name}_answer_labels.json")
            translated_files = txt_files[key]["Translations"]
            extended_mintaka_path = f"{d_path.replace('.json', '_extended2.json')}"
            print(f"Extending mintaka json with translated questions and labels...")
            extend_mintaka_json(d_path, answer_labels, translated_files, extended_mintaka_path)
            print(f"Succuesfully extended the mintaka {key} dataset and saved to {extended_mintaka_path}")
            answer_labels = open_json(f'./outputs/answer_labels/{dataset_name}_answer_labels.json')
            print(f"Generating answer label sheet for {dataset_name}...")
            generate_answer_label_sheet(answer_labels, dataset_name)
            print(f"Answer label sheet for {dataset_name} generated successfully.")
            print(f"Pipeline for {key} dataset completed.")

if __name__ == "__main__":
    run_pipeline(data_paths, ["de"])
