import random
from openpyxl import Workbook
from Services.file_service import open_txt
import os

def generate_random_translation_sampling_sheet(txt_data_object, samples):
    """
    Randomly samples lines from multiple text files and writes them to an Excel file.
    
    Args:
        txt_files (object on format {language_header : path_to_txt_file}): A dictionary with language headers as keys and paths to txt files as values.
        sampling_rate (float): The rate at which to sample lines from the files.
    """
    
    # Get the directory of the current script
    script_dir = os.path.dirname(__file__)
    
    # Read the English file
    english_file = txt_data_object["English"]
    english_lines = open_txt(os.path.join(script_dir, english_file))
    
    # Read all translation files and store lines in a dictionary
    all_lines = {"English": english_lines}
    for language, file in txt_data_object["Translations"].items():
        lines = open_txt(os.path.join(script_dir, file))
        all_lines[language] = lines
    
    # Ensure all files have the same number of lines
    num_lines = len(english_lines)
    for lines in all_lines.values():
        print(len(lines))
        if len(lines) != num_lines:
            raise ValueError("All files must have the same number of lines")
    
   
    if(num_lines > samples):
        raise ValueError("Number of samples must be less than the number of lines in the file")
    
    # Randomly select indices
    sampled_indices = random.sample(range(num_lines), samples)
    
    # Create a Workbook
    wb = Workbook()
    
    # Create a sheet for each translation language
    for language, lines in txt_data_object["Translations"].items():
        ws = wb.create_sheet(title=f"{language} samples")
        
        # Add headers
        ws.append(["English", language])
        
        # Collect sampled lines and add to the sheet
        for idx in sampled_indices:
            row = [all_lines["English"][idx].strip(), all_lines[language][idx].strip()]
            ws.append(row)
    
    # Remove the default sheet created by openpyxl
    del wb["Sheet"]
    
    # Save the workbook
    output_path = os.path.join(script_dir, "../outputs/sampling/sampled_translations.xlsx")
    wb.save(output_path)
    print(f"Samples written to {output_path}")
