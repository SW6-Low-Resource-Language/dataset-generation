from SPARQLWrapper import SPARQLWrapper, SPARQLExceptions, JSON
import time

query_find_labels_template = """SELECT ?entity ?label WHERE {
  VALUES ?entity { ENTITY_IDS }
  ?entity rdfs:label ?label .
  FILTER(LANG_STR)
}
"""
"LANG(?label) = '{lang}'"


    
def queryWikidata(query):
    """
    Executes a SPARQL query against the Wikidata SPARQL endpoint and returns the results in JSON format.
    Args:
        query (str): The SPARQL query string to be executed.
    Returns:
        dict: The results of the SPARQL query in JSON format.
    """
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    try:
        results = sparql.query().convert()
        return results
    except SPARQLExceptions.EndPointInternalError as e:
        print(f"An internal error occurred while querying Wikidata: {e}")
        print(f"Headers: {e.response.headers}")
    except SPARQLExceptions.QueryBadFormed as e:
        print(f"The query is malformed: {e}")
        print(f"Headers: {e.response.headers}")
    except Exception as e:
        print(f"An error occurred while querying Wikidata: {e}")
        if hasattr(e, 'response') and hasattr(e.response, 'headers'):
            print(f"Headers: {e.response.headers}")
    return None

def get_wikidata_labels(answer_entities, lang_codes=["da", "bn"]):
    """
    Retrieves labels for given Wikidata entities in specified languages.
    Args:
        answer_entities (dict): A dictionary where keys are question IDs and values are lists of entity IDs.
        lang_codes (list, optional): A list of language codes for which labels should be retrieved. Defaults to ["da", "bn"].
    Returns:
        dict: A nested dictionary where the first level keys are entity ID's, and the second level keys are language codes. The values are the corresponding labels for the entities in the specified languages.
    """
    entity_lan_labels_map = {}
    for answer_entities_ids in answer_entities.values():
        for entity in answer_entities_ids:
            entity_lan_labels_map[entity] = {} 
            for lan in lang_codes:
                entity_lan_labels_map[entity][lan] = None

    inBatch = 0
    batch = []
    
    for answer_entities_ids in answer_entities.values():
        if inBatch == 50:
            labels = get_wikidata_labels_for_answer(batch, lang_codes)
            inBatch = 0
            batch = []
            time.sleep(0.5)
            for entity, lan_labels in labels.items():
                for lan, label in lan_labels.items():
                    entity_lan_labels_map[entity][lan] = label
        else:
            batch.extend(answer_entities_ids)
            inBatch += 1 
    
    return entity_lan_labels_map


def get_wikidata_labels_for_answer(entities, lang_codes):
    """
    Retrieves labels for given Wikidata entities in specified languages.

    Args:
        entities (list of str): A list of Wikidata entity IDs.
        lang_codes (list of str): A list of language codes to retrieve labels for.
    Returns:
        dict: A dictionary where keys are entity IDs and values are dictionaries with language codes as keys and labels as values.
    """

    entity_ids = " ".join(f"wd:{entity}" for entity in entities)
    lang_str = " || ".join(f"LANG(?label) = '{lang}'" for lang in lang_codes)
    print(f"finding labels for entities: {entity_ids} in languages: {lang_codes}")
    query = query_find_labels_template.replace("ENTITY_IDS", entity_ids).replace("LANG_STR", lang_str)
    results = queryWikidata(query)
    labels = {}
    for result in results["results"]["bindings"]:
        entity = result["entity"]["value"].split("/")[-1]
        lang_code = result["label"]["xml:lang"]
        label = result["label"]["value"]
        if entity not in labels:
            labels[entity] = {}
        labels[entity][lang_code] = label
    return labels

# Example usage
if __name__ == "__main__":
    entities = ["Q53945", "Q42", "Q1", "Q2", "Q3", "Q4", "Q430658"]
    labels = get_wikidata_labels_for_answer(entities, ["da", "bn"])
    print(labels)