from shared_utils.file_service import open_json

data = open_json(r"outputs\answer_labels\mintaka_dev_answer_labels.json")
print(data)