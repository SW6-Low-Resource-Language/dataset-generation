import os
from dotenv import load_dotenv
import deepl

# Load environment variables from .env file
load_dotenv()

# Get the DeepL auth key from environment variables
auth_key = os.getenv("DEEPL_AUTH_KEY")
deepl_client = deepl.DeepLClient(auth_key)

def deepl_translate_large_text_file(input_path, output_path, target_language="DA"):
    try:
        # Using translate_document_from_filepath() with file paths 
        deepl_client.translate_document_from_filepath(
            input_path,
            output_path,
            target_lang=target_language,
        )
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

