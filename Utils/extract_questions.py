from Utils.amount_chars import amount_chars
from Services.file_service import open_json, write_json

# util for extracting all the questions in english from the mintaka dataset
def extract_questions(data_path, output_path):
    """
    Extracts questions from a JSON file, counts the total number of characters in all questions,
    and saves the questions along with the character count to an output JSON file.
    Args:
        data_path (str): The file path to the input JSON file containing the data.
        output_path (str): The file path to the output JSON file where the extracted questions and character count will be saved.
    Returns:
        dict: A dictionary containing the extracted questions and the total character count.
    """
    data = open_json(data_path)
    questions = {item['id']: item['question'] for item in data}
    chars = amount_chars(questions.values())
    print(f"Extracted {len(questions)} questions with a total of {chars} characters")
    questions = {"questions" : questions, "char_count": chars}
    
    # Write the new dictionary to the output file
    write_json(questions, output_path)
    print(f"Saved {len(questions['questions'])} questions to {output_path} for mapping purposes and overview")

    return questions



