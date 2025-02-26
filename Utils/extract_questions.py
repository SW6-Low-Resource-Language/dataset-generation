from Utils.amount_chars import amount_chars
from Services.file_service import open_json, write_json

# util for extracting all the questions in english from the mintaka dataset
def extract_questions(data_path, output_path):
    data = open_json(data_path)
    questions = {item['id']: item['question'] for item in data}
    chars = amount_chars(questions.values())
    print(f"Extracted {len(questions)} questions with a total of {chars} characters")
    questions = {"questions" : questions, "char_count": chars}
    # Write the new dictionary to the output file
    write_json(questions, output_path)
    print(f"Saved {len(questions['questions'])} questions to {output_path} for mapping purposes and overview")

    return questions



