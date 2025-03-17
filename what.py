from Services.wikidata import find_wikidata_entity_from_string
data_sheets = {
    "dev" : "./data/mintaka_dev.json",
    "test" : "./data/mintaka_test.json",
    "train" : "./data/mintaka_train.json"
}

""" data = data_sheets["dev"]
mentions = extract_null_answer_mentions_from_data(data)
entities = get_wikidata_enities_from_strings(mentions.values())
print(entities) """
search_string = "Rainbow Road (disambiguation)"
entity = find_wikidata_entity_from_string(search_string) 
print(entity)
   