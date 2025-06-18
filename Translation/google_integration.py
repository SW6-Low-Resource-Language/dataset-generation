# Imports the Google Cloud Translation library
import os
from dotenv import load_dotenv
from google.cloud import translate_v3
from shared_utils.file_service import open_txt, write_txt

# This function translates a txt file line by line with google api, we experimented with translating large chunks of text at the same time but it lead to newline alignments issues, so this is the safe approach.
def google_translate_line_by_line(input_path, output_path, target_language="bn"):
    """
    Translates the content of a large text file line by line using Google Cloud Translation API and saves the translated text to an output file.
    Args:
        input_file (str): The path to the input text file to be translated.
        output_file (str): The path to the output text file where the translated text will be saved.
        target_language (str, optional): The target language code for translation (default is "da" for Danish).
    """
    load_dotenv()
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable is not set.")
    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{PROJECT_ID}/locations/global"

    lines = open_txt(input_path)    
    translated_lines = []
    count = 0
    lines_len = len(lines)
    for line in lines:
        print(f"Translating line {count + 1} of {lines_len}")
        count += 1
        response = client.translate_text(
            parent=parent,
            contents=[line],
            mime_type="text/plain",
            target_language_code=target_language,
            source_language_code="en-US",
        )
        translated_text = response.translations[0].translated_text.replace("\n", "")

        translated_lines.append(translated_text)

    write_txt(translated_lines, output_path)
    print(f"Translation saved to {output_path}")

def google_translate_text(text, target_language):
    """
    Translates a text string using the Google Cloud Translation API.
    Args:
        text (str): The text to be translated.
        target_language (str): The target language code for translation.
    Returns:
        str: The translated text.
    """
    load_dotenv()
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable is not set.")
    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{PROJECT_ID}/locations/global"
    response = client.translate_text(
        parent=parent,
        contents=[text],
        mime_type="text/plain",
        target_language_code=target_language,
        source_language_code="en-US",
    )
    translated_text = response.translations[0].translated_text
    return translated_text

# Example usage of the functions
if __name__ == "__main__":
    text = google_translate_text("9ace9041: What is the fourth book in the Twilight series?", "bn")
    print(text)
    