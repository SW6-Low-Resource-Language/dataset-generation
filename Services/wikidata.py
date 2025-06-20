from SPARQLWrapper import SPARQLWrapper, SPARQLExceptions, JSON
import wikipedia
from wikipedia.exceptions import DisambiguationError, PageError 
from shared_utils.file_service import open_json
import time


query_find_labels_template = """SELECT ?entity ?label WHERE {
  VALUES ?entity { ENTITY_IDS }
  ?entity rdfs:label ?label .
  FILTER(LANG_STR)
}
"""
"LANG(?label) = '{lang}'" 

query_find_dbpedia_page = """select ?e where
{
<http://dbpedia.org/resource/PAGE_IDENT> owl:sameAs ?e .
FILTER contains(str(?e), "wikidata")
}
"""

def find_wikidata_entity_from_string(search_string):
    """
    Attempts to find the Wikidata entity ID corresponding to a given search string.
    Args:
        search_string (str): The string to search for in Wikipedia and resolve to a Wikidata entity.
    Returns:
        str or None: The Wikidata entity ID (e.g., 'Q529026') if found, otherwise None.
    """
    wp_search = wikipedia.search(search_string)

    print(f"searching for: {search_string}")
    print(f"found: {wp_search}")
    if not wp_search:
        print(f"Could not find a Wikipedia page for the search string: {search_string}")
        return None
    try:
        page = wikipedia.page(wp_search[0], auto_suggest=False)
    except DisambiguationError as e:
        print(f"DisambiguationError: may refer to:")
        disambiguation_options = e.options
        print(disambiguation_options)
        return None
    except PageError as e:
        print(f"PageErro' does not match any pages. {e}")
        return None
    
    url = page.url
    ident = url.split("/")[-1]
    query = query_find_dbpedia_page.replace("PAGE_IDENT", ident)
    print(f"querying dbpedia for: {query}")
    db_search = queryDBpedia(query)
    if not db_search:
        print(f"Could not find a DBpedia entity for the search string: {search_string}")
        return
    if not db_search['results']['bindings']:
        print(f"Could not find a Wikidata entity for the search string: {search_string}")
        return None
    

    entity_id = db_search['results']['bindings'][0]['e']['value'].split("/")[-1]
    # {'head': {'link': [], 'vars': ['e']},
    # 'results': 
    #   {'distinct': False, 
    #   'ordered': True, 
    #   'bindings': 
    #       [{'e': 
    #           {'type': 'uri', 
    #           'value': 'http://www.wikidata.org/entity/Q529026'}}]}}#
    #results=> bindings[] => idx 0 => e => value => bingo.split
    # use identifier on datapedia 
    return entity_id


def queryDBpedia(query):
    """
    Executes a SPARQL query against the DBpedia endpoint and returns the results in JSON format.

    Args:
        query (str): The SPARQL query string to be executed on the DBpedia endpoint.

    Returns:
        dict: The results of the SPARQL query in JSON format if successful.

    Raises:
        Prints error messages for internal endpoint errors, malformed queries, or other exceptions.
        Does not raise exceptions directly; errors are logged to the console.
    """
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    try:
        results = sparql.query().convert()
        return results
    except SPARQLExceptions.EndPointInternalError as e:
        print(f"An internal error occurred while querying DBpedia: {e}")
        print(f"Headers: {e.response.headers}")
    except SPARQLExceptions.QueryBadFormed as e:
        print(f"The query is malformed: {e}")
        print(f"Headers: {e.response.headers}")
    except Exception as e:
        print(f"An error occurred while querying DBpedia: {e}")
        if hasattr(e, 'response') and hasattr(e.response, 'headers'):
            print(f"Headers: {e.response.headers}")
    
def queryWikidata(query):
    """
    Executes a SPARQL query against the Wikidata SPARQL endpoint and returns the results in JSON format.
    Args:
        query (str): The SPARQL query string to be executed.
    Returns:
        dict: The results of the SPARQL query in JSON format.
    """
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent="Extending_mintaka/1.0 (Lassemgp@gmail.com)" )
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)  # Set a proper User-Agent

    retries = 5
    for attempt in range(retries):
        try:
            results = sparql.query().convert()
            return results
        except SPARQLExceptions.EndPointInternalError as e:
            print(f"Attempt {attempt + 1}/{retries}: An internal error occurred while querying Wikidata: {e}")
        except SPARQLExceptions.QueryBadFormed as e:
            print(f"Attempt {attempt + 1}/{retries}: The query is malformed: {e}")
            break  # No point in retrying if the query is malformed
        except Exception as e:
            if hasattr(e, 'response') and e.response.status == 429:  # Handle rate-limiting
                retry_after = int(e.response.headers.get("Retry-After", 5))  # Default to 5 seconds if not provided
                print(f"Rate limit exceeded. Retrying after {retry_after} seconds...")
                time.sleep(retry_after)
            else:
                print(f"Attempt {attempt + 1}/{retries}: An error occurred while querying Wikidata: {e}")
        if attempt < retries - 1:
            print(f"Retrying in 5 seconds...")
            time.sleep(5)
    return None

def get_wikidata_labels(answer_entities, map_path, lang_codes=["da", "bn"]):
    """
    Retrieves labels for given Wikidata entities in specified languages.
    Args:
        answer_entities (dict): A dictionary where keys are question IDs and values are lists of entity IDs.
        lang_codes (list, optional): A list of language codes for which labels should be retrieved. Defaults to ["da", "bn"].
    Returns:
        dict: A nested dictionary where the first level keys are entity ID's, and the second level keys are language codes. The values are the corresponding labels for the entities in the specified languages.
    """
    entity_lan_labels_map = open_json(map_path)
    for answer_entities_ids in answer_entities.values():
        for entity in answer_entities_ids:
            if entity not in entity_lan_labels_map:
                entity_lan_labels_map[entity] = {} 
            for lan in lang_codes:
                entity_lan_labels_map[entity][lan] = None

    inBatch = 0
    batch = []
    batch_size = 100
    
    for answer_entities_ids in answer_entities.values():
        batch.extend(answer_entities_ids)
        inBatch += 1 
        if inBatch == batch_size:
            labels = get_wikidata_labels_for_answer(batch, lang_codes)
            inBatch = 0
            batch = []
            time.sleep(2)
            for entity, lan_labels in labels.items():
                for lan, label in lan_labels.items():
                    entity_lan_labels_map[entity][lan] = label
            
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
    if not results:
        return labels
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
    labels = get_wikidata_labels_for_answer(["Q42", "Q1"], ["tr"])
    print(labels)

