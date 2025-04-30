from shared_utils.file_service import open_json
from Utils.wikidata_label_coverage import test_label_coverage

data = open_json(r"outputs\answer_labels\mintaka_train_answer_labels.json")
print(data)
test_label_coverage(data, languages=["fi", "da", "bn"])