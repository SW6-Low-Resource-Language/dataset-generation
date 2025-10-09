import requests

libretranslate_address = "http://localhost:5000"

def libretranslate_translate_text(text, target_language="sv"):
    endpoint = libretranslate_address+"/translate"
    r = requests.post(endpoint,
                      data ={
                      "q" : text,
                      "source" : "en",
                      "target": target_language
                      })
    #if r.status_code != 200:
    #    raise RuntimeError

    return r.text

def libretranslate_translate_large_text_file(input_path, output_path, target_language="fi"):
    endpoint = f"{libretranslate_address}/translate_file"
    with open(input_path, "rb") as infile:
        files = {"file": infile}
        data = {
            "source": "en",
            "target": target_language
        }
        # First request: get URL to translated file
        response = requests.post(endpoint, files=files, data=data)
        if response.status_code != 200:
            raise RuntimeError(f"Translation failed: {response.status_code} {response.text}")

        result = response.json()
        translated_file_url = result.get("translatedFileUrl")
        if not translated_file_url:
            raise RuntimeError(f"No translatedFileUrl in response: {response.text}")

        # Second request: download the translated file
        download_response = requests.get(translated_file_url)
        if download_response.status_code != 200:
            raise RuntimeError(f"Failed to download translated file: {download_response.status_code} {download_response.text}")

        with open(output_path, "wb") as outfile:
            outfile.write(download_response.content)

if __name__ == "__main__":
    input = "This is a test sentence"
    output = libretranslate_translate_text(input, target_language="sv")
    print(output)
