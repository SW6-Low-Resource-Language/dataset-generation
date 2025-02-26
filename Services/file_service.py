import json

def open_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def write_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def open_txt(file_path, seperator = '\n'):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = f.read().split(seperator)
    return data

def write_txt(data, file_path, seperator = '\n'):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(seperator.join(data))