


def test_label_coverage(answer_entity_map, languages=None):
    """
    Analyzes the coverage of Wikidata labels for a given set of entities and languages.

    Args:
        labels_array (dict): A dictionary where keys are entity IDs and values are dictionaries
                             mapping language codes to their corresponding labels (or None if no label exists).
        languages (list, optional): A list of language codes to analyze. If None, it will try and determine the keys from the object

    Returns:
        None: Prints the total number of labels, null labels, and the percentage of found labels
              for each language to the console.
    """
    if languages is None:
        for lang in answer_entity_map.values():
            languages = list(lang.keys())
            break

    g_label_map = {lang : {"got_label": 0, "got_null_label": 0} for lang in languages}
    for entity, lan_labels in answer_entity_map.items():
        for lan, label in lan_labels.items():
            if label is None:
                g_label_map[lan]["got_null_label"] += 1
            else:
                g_label_map[lan]["got_label"] += 1
    for lang, label_map in g_label_map.items():
        print(f"Total labels: {label_map['got_label'] + label_map['got_null_label']}")
        print(f"Language: {lang}")
        print(f"Got label: {label_map['got_label']}")
        print(f"Got null label: {label_map['got_null_label']}")
        print(f"Percentage of found labels: {label_map['got_label'] / (label_map['got_label'] + label_map['got_null_label']) * 100:.2f}%")
        print("")