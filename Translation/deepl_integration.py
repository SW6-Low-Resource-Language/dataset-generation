import os
from dotenv import load_dotenv
import deepl

# Load environment variables from .env file
load_dotenv()

# Get the DeepL auth key from environment variables
auth_key = os.getenv("DEEPL_AUTH_KEY")

# Check if the auth key is loaded correctly
if auth_key is None:
    raise ValueError("DEEPL_AUTH_KEY not found in environment variables")

# Initialize the DeepL translator
translator = deepl.Translator(auth_key)

# Example translation
result = translator.translate_text("What is the fourth book in the Twilight series?", target_lang="DA")
print(result.text) # Hvad er den fjerde bog i Twilight-serien?