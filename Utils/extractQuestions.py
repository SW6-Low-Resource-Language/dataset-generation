import json
data_path = '../data/mintaka_dev.json'
output_path = '../data/id2question.json'
# util for extracting all the questions in english from the mintaka dataset
def extract_questions(data_path, output_file):
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    questions = {item['id']: item['question'] for item in data}

    # Write the new dictionary to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=4)

# extract_questions(data_path, output_path)

