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
    """Splits text into chunks under max_size bytes"""
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
            target_language_code=target_language
        )
        translated_chunks.append(response.translations[0].translated_text)

    print(translated_chunks)
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("\n".join(translated_chunks))

    print(f"Translation saved to {output_file}")

google_translate_large_text_file("./test-input.txt", "./test-output.txt", "bn")