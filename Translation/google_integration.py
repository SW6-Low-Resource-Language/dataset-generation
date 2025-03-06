# Imports the Google Cloud Translation library
import os
from dotenv import load_dotenv
from google.cloud import translate_v3

load_dotenv()
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
print(PROJECT_ID)

# Google API can only translate text up to 30,000 characters at a time
# This function splits the text into chunks under 30,000 characters
def chunk_text(text, max_size=30000):
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

def google_translate_large_text_file(input_file, output_file, target_language="da"):
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
    charLen = 0
    for chunk in chunks:
        charLen += chunk.count("?")
        print(len(chunk))
        response = client.translate_text(
            parent=parent,
            contents=[chunk],
            mime_type="text/plain",
            target_language_code=target_language
        )
        # "Google sometimes returns double newlines, so we replace them with single newlines"
        translated_text = response.translations[0].translated_text.replace("\n\n", "\n")
        translated_chunks.append(translated_text)

    print(translated_chunks)
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("\n".join(translated_chunks))

    print(f"Translation saved to {output_file}")
    print(f"Total characters: {charLen}")
    
google_translate_large_text_file("./test-input.txt", "./test-output.txt", "da")