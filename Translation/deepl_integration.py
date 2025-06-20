import os
from dotenv import load_dotenv
import deepl




def deepl_translate_text(text, target_language="fi"):
    """
    Translates a text string using the DeepL API.
    Args:
        text (str): The text to be translated.
        target_language (str, optional): The target language code for translation. Defaults to "DA" (Danish).
    Returns:
        str: The translated text.
    """
    try:
        # Using translate_text() with a text string
        translated_text = deepl_client.translate_text(
            text,
            target_lang=target_language.upper(),
        )
        return translated_text
    except deepl.DeepLException as error:
        # Errors during upload raise a DeepLException
        print(error)


def deepl_translate_large_text_file(input_path, output_path, target_language="fi"):
    """
    Translates a large text file using the DeepL API and saves the translated file to the specified output path.
    Args:
        input_path (str): The path to the input file to be translated.
        output_path (str): The path where the translated file will be saved.
        target_language (str, optional): The target language code for translation. Defaults to "DA" (Danish).
    """
      # Load environment variables from .env file
    load_dotenv()
    # Get the DeepL auth key from environment variables
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is not set.")
    deepl_client = deepl.DeepLClient(auth_key)
    try:
        # Using translate_document_from_filepath() with file paths 
        deepl_client.translate_document_from_filepath(
            input_path,
            output_path,
            target_lang=target_language.upper(),
        )
        print(f"DeepL Translated file saved to {output_path}")
    except deepl.DocumentTranslationException as error:
        # If an error occurs during document translation after the document was
        # already uploaded, a DocumentTranslationException is raised. The
        # document_handle property contains the document handle that may be used to
        # later retrieve the document from the server, or contact DeepL support.
        doc_id = error.document_handle.id
        doc_key = error.document_handle.key
        print(f"Error after uploading ${error}, id: ${doc_id} key: ${doc_key}")
    except deepl.DeepLException as error:
        # Errors during upload raise a DeepLException
        print(error)


if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()
    # Get the DeepL auth key from environment variables
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is not set.")
    deepl_client = deepl.DeepLClient(auth_key)
    input = "Hej hvordan har du det?"
    output = deepl_translate_text(input, target_language="fi")
    print(output)
