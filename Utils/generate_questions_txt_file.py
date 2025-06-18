from shared_utils.file_service import write_txt


def generate_questions_txt_file(json_map, output_path, seperator = '\n'):
    """
    Generates a translation file from a JSON map and saves it to the specified output path.

    Args:
        json_map (dict): A dictionary containing the data to be written to the file.
        output_path (str): The path where the output file will be saved.
        seperator (str, optional): The separator to use between questions in the output file. Defaults to '\n'.
    """
    data = json_map['questions'].values()
    write_txt(data, output_path, seperator)
    return data
    