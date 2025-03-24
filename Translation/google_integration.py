# Imports the Google Cloud Translation library
import os
from dotenv import load_dotenv
from google.cloud import translate_v3
from Services.file_service import open_txt, write_txt

load_dotenv()
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
print(PROJECT_ID)

# Google API can only translate text up to 30,000 characters at a time
# This function splits the text into chunks under 20,000 characters
def chunk_text(text, max_size=20000):
    """
    Splits the input text into chunks, each under the specified maximum size in bytes.

    Args:
        text (str): The input text to be split into chunks.
        max_size (int, optional): The maximum size of each chunk in bytes. Defaults to 30000.

    Returns:
        list: A list of text chunks, each under the specified maximum size.
    """
    chunks = []
    current_chunk = ""
    for line in text.split("\n"):
        if len(current_chunk) + len(line) + 1 > max_size:
            chunks.append(current_chunk)
            current_chunk = line
        else:
            current_chunk += "\n" + line if current_chunk else line

    if current_chunk:
        chunks.append(current_chunk)

    return chunks

def google_translate_chunks(input_file, output_file, target_language="bn"):
    """
    Translates the content of a large text file using Google Cloud Translation API and saves the translated text to an output file.
    Args:
        input_file (str): The path to the input text file to be translated.
        output_file (str): The path to the output text file where the translated text will be saved.
        target_language (str, optional): The target language code for translation (default is "da" for Danish).
    """
    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{PROJECT_ID}/locations/global"

    with open(input_file, "r", encoding="utf-8") as file:
        text = file.read()
    chunks = chunk_text(text)
    translated_chunks = []
    for chunk in chunks:
        response = client.translate_text(
            parent=parent,
            contents=[chunk],
            mime_type="text/plain",
            target_language_code=target_language,
            source_language_code="en-US",
        )
        
        # "Google sometimes returns double newlines in chunks, so we replace them with single newlines"
        translated_text = response.translations[0].translated_text.replace("\n\n", "\n")
        translated_chunks.append(translated_text)
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("\n".join(translated_chunks))

    print(f"Translation saved to {output_file}")


# This function translates a txt file line by line with google api, it's significantly slower than the chunking method but provides correct output (content was lost in translating to bn with chunks)
def google_translate_line_by_line(input_path, output_path, target_language="bn"):
    """
    Translates the content of a large text file line by line using Google Cloud Translation API and saves the translated text to an output file.
    Args:
        input_file (str): The path to the input text file to be translated.
        output_file (str): The path to the output text file where the translated text will be saved.
        target_language (str, optional): The target language code for translation (default is "da" for Danish).
    """
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
    