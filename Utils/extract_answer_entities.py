from Services.file_service import open_json, write_json
import os


def extract_answer_entities(data_path, output_path = None):
    if output_path is None:
        output_path = f'./outputs/answer_entities_maps/{os.path.basename(data_path.replace(".json",""))}_answer_entities.json'
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
    write_json(id_answer_entities_map, output_path)
    return id_answer_entities_map
        

            



