from Services.file_service import open_json, write_json
from Services.wikidata import find_wikidata_entity_from_string


def run_analysis(data_sheets):
    results = {}
    results["all"] = {}
    found_entities = {}
    found_entities["all"] = {}
    mention_entity_object = {}
    for data_name, data_path in data_sheets.items():
        mention_entity_object[data_name] = {}
        found_entities[data_name] = {}
        found_entities[data_name]["total"] = 0
        results[data_name] = {}
        results[data_name]["total"] = 0
        
        data = open_json(data_path)
        for entry in data:
            cat = entry["category"]
            complexity = entry["complexityType"]
            answer = entry["answer"]
            answerType = answer["answerType"]
            if answerType == "entity" and answer["answer"] == None: 
                results[data_name]["total"] += 1
                
                if cat not in results["all"]:
                    results["all"][cat] = {"total": 0}
                if complexity not in results["all"][cat]:
                    results["all"][cat][complexity] = 0
                if cat not in results[data_name]:
                    results[data_name][cat] = {}
                if complexity not in results[data_name][cat]:
                    results[data_name][cat][complexity] = 0
                results[data_name][cat][complexity] += 1
                results["all"][cat][complexity] += 1
                results["all"][cat]["total"] += 1

                    # print(entry)
                id = entry["id"]
                question = entry["question"]
                mention = answer["mention"]
                entity = find_wikidata_entity_from_string(mention)
                if entity:
                    found_entities[data_name]["total"] += 1
                    if cat not in found_entities["all"]:
                        found_entities["all"][cat] = {"total": 0}
                    if complexity not in found_entities["all"][cat]:
                        found_entities["all"][cat][complexity] = 0
                    if cat not in found_entities[data_name]:
                        found_entities[data_name][cat] = {}
                    if complexity not in found_entities[data_name][cat]:
                        found_entities[data_name][cat][complexity] = 0
                    found_entities[data_name][cat][complexity] += 1
                    found_entities["all"][cat][complexity] += 1
                    found_entities["all"][cat]["total"] += 1

                mention_entity_object[data_name][id] = {"question": question, "mention": mention, "entity": entity, "category": cat, "complexity": complexity}

                
                
    print("The analysis is now done and results will be written to JSONS")
    write_json(results, "./outputs/missing_entities.json")
    print("Stats for missing answer entities written to missing_entities.json")
    write_json(found_entities, "./outputs/found_entities.json")
    print("Stats for amount of missing entites we could find a potential wikidata ID for based on the mention are to written to found_entities.json")
    write_json(mention_entity_object, "./outputs/mention_entity_object.json")
    print("An overview of the mentions and the entities we found based on the mentions are written to mention_entity_object.json")
   