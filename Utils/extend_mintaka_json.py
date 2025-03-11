from Services.file_service import open_json, write_json, open_txt

def extend_mintaka_json(data_path, answer_labels, translated_files):
    """
    Extends the mintaka json with translated questions and relevant labels.
    Args:
        data_path (str): Path to the mintaka json file.
        answer_labels (dict): A dictionary where keys are entity ID's, and the second level keys are language codes. The values are the corresponding labels for the entities in the specified languages.
        translated_files (dict): A dictionary where the keys are language codes and the values are paths to the translated questions.
    """
    mintaka_data = open_json(data_path)
    lang_translations = {}
    for lang, file_path in translated_files.items():
        open_txt(file_path)
        lang_translations[lang] = open_txt(file_path)

    for index, entry in enumerate(mintaka_data):
        for lang, translations in lang_translations.items():
            entry['translations'][lang] = translations[index]

        answer = entry['answer']
        answer_type = answer['answerType']
        # Only entity and numerical answerTypes have enitites with labels
        if (answer_type not in ['entity', 'numerical']):
            continue
        entities_key = answer_type == 'entity' and 'answer' or 'supportingEnt'

        # Some numerical answers have no supporting entities
        if entities_key not in answer:
            continue
        answer_entities = answer[entities_key]
        # Some "entity" answers have no refferences to wikidata entities
        if not answer_entities:
            continue

        for entity in answer_entities:
            entity_id = entity['name']
            entity_labels = answer_labels.get(entity_id)
            for lang, label in entity_labels.items():
                entity["label"][lang] = label


    write_json(mintaka_data, f"{data_path.replace('.json', '_extended.json')}")
        


   
    """ write_json(data, data_path) """