from shared_utils.file_service import open_json, write_json
import os


def extract_answer_entities(data_path): 
    """
    Extracts a mapping from item IDs to lists of entity names (WikiIDs) from a dataset.
    Args:
        data_path (str): Path to the JSON file containing the dataset. The dataset should be a list of items,
            each with an 'id' and an 'answer' field. The 'answer' field should contain an 'answerType' key,
            and depending on its value ('entity' or 'numerical'), may contain entity references.
    Returns:
        dict: A dictionary mapping each item's 'id' to a list of entity names (WikiIDs) extracted from the answer.
            Only items with 'entity' or 'numerical' answer types and valid entity references are included.
    """
    data = open_json(data_path)
    id_answer_entities_map = {}
    for item in data:
        answer = item['answer']
        answer_type = answer['answerType']
        # Only entity and numerical answerTypes have enitites with labels
        if (answer_type not in ['entity', 'numerical']):
            continue

        id = item['id']
        entities_wikiIDs = []
        entities_key = answer_type == 'entity' and 'answer' or 'supportingEnt'

        # Some numerical answers have no supporting entities
        if entities_key not in answer:
            continue
        answer_entities = answer[entities_key]
        # Some "entity" answers have no refferences to wikidata entities
        if not answer_entities:
            continue

        for entity in answer_entities:
            entities_wikiIDs.append(entity['name'])
        id_answer_entities_map[id] = entities_wikiIDs
    
    return id_answer_entities_map
        

            



