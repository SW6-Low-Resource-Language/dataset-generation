from Services.file_service import write_txt


def generate_translation_file(json_map, output_path, seperator = '\n'):
    data = json_map['questions'].values()
    write_txt(data, output_path, seperator)
    print(f"Saved {len(data)} questions to {output_path} for translation")
    