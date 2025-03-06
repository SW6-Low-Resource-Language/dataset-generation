from Services.file_service import open_json, write_json


def extract_answer_entities(data_path):
    data = open_json(data_path)
    print(data[0])



