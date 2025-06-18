from openpyxl import Workbook

def generate_answer_label_sheet(answer_labels, dataset_name): 
    """
    Generates an Excel sheet containing answer labels for entities in multiple languages.

    Args:
        answer_labels (dict): A dictionary where each key is an entity ID (str) and each value is another dictionary
                              mapping language codes (str) to their corresponding label (str) for that entity.
                              Example:
                              {
                                  "Q42": {"en": "Douglas Adams", "fr": "Douglas Adams"},
                                  "Q1": {"en": "Universe", "fr": "Univers"}
                              }
        dataset_name (str): The name of the dataset, used to name the output Excel file.

    Functionality:
        - Creates an Excel workbook with a sheet titled "Answer labels".
        - The first row contains headers: "Entity ID", one column per language (e.g., "en-label", "fr-label"), and "Wikidata URL".
        - Each subsequent row contains the entity ID, its labels in each language, and a link to its Wikidata page.
        - Saves the Excel file to "./outputs/answer_labels/{dataset_name}_answer_labels_sheet.xlsx".
    """
    wb = Workbook()
    ws = wb.active
    ws.title = "Answer labels"
    headers = ["Entity ID"]
    lang_index_map = {}
    for index, lang in enumerate(list(answer_labels.values())[0].keys()):  # Convert to list to access the first element
        print(f"Adding header for {lang}")
        headers.append(f"{lang}-label")
        lang_index_map[lang] = index + 1
    headers.append("Wikidata URL")
    ws.append(headers)
    for entity_id, lang_labels in answer_labels.items():
        row = [None] * len(headers)  # Dynamically size the row based on the headers
        row[0] = entity_id
        for lang, label in lang_labels.items():
            if lang in lang_index_map:  # Ensure the language exists in the map
                row[lang_index_map[lang]] = label
        row[-1] = f"https://www.wikidata.org/wiki/{entity_id}"
        ws.append(row)
    wb.save(f"./outputs/answer_labels/{dataset_name}_answer_labels_sheet.xlsx")
    print(f"Answer labels sheet for {dataset_name} has been generated")
