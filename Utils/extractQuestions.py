import json
from Utils.amountChars import amountChars

# util for extracting all the questions in english from the mintaka dataset
def extract_questions(data_path, output_path):
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    questions = {item['id']: item['question'] for item in data}
    chars = amountChars(questions.values())
    print(f"Extracted {len(questions)} questions with a total of {chars} characters")
    questions = {"questions" : questions, "char_count": chars}
    # Write the new dictionary to the output file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=4)



