# Purpose

The purpose of this repository is to extend the mintaka dataset to new languages on the basis of the [Mintaka Dataset](https://github.com/amazon-science/mintaka). 


## Process
The process of extending the dataset consists of:
- Translating the orgininal English questions to the language of choice
- Extracting wikidata entity labels in language of choice for all answer entities


## Requirements
to install the dependencies write:
`pip install -r requirements.txt`
to update dependencies write:
`pip freeze > requirements.txt`

## How to
 
## env variables
in order for the pipeline to function you need to have the following api keys specified in a an .env file located in the root folder
- DEEPL_AUTH_KEY - https://www.deepl.com/en/your-account/keys
- GOOGLE_CLOUD_PROJECT - ID for your project with the translator api enabled
- Note: For google translation ADC needs to be configured, you're also free to implement your own translation functions and include corresponding env keys.

## Extending to a new language 
In order to extend the mintaka dataset to new languages, you need to modify the main.py file as follows, 
1. Specify the dataset splits you wish to extend, if you just want to start out trying to extend the dev split to the new language you can assign the data_paths dict as below.
`data_paths = {
    'dev': './data/mintaka_dev.json'`
if you wish to do it for all splits in one run you should specify data_paths like:
`data_paths = {
    'dev': './data/mintaka_dev.json,
   'train': './data/mintaka_train.json,
   'test': './data/mintaka_dev.json,
}
   '`
3. Next you need to specify the languages you wish to extend to, this is done in the buttom of the file when invoking the run_pipeline function. If you wish you extend to lets say swedish you would write
   `run_pipeline(data_paths, ["sv"])`

4. The final thing you need to do is to specify the translator to use for the given language, this is done within the run_pipeline function in the translation_functions dict, here you need to map the language code to a function accepting the path to a txt file containing the questions, a destination path on where to output a txt file containing the translated questions and the language code. Extending the current implentation to e.g swedish would then result in.
`translation_functions = {
            "bn": google_translate_line_by_line,
            "da": deepl_translate_large_text_file,
            "fi": deepl_translate_large_text_file,
            "sv": deepl_translate_large_text_file, 
        }`

Note: There is implemented 3 control variables in the main.py file `translate`, `samples` and `extend_mintaka` which can be used to control the flow of the pipeline, so if you want to only translate the questions and have time to check them before moving on to extracting labels and extending the dataset, you can set extend_mintaka to `false` and specify the amount of random translation samples to be generated. Afterwards you can set `translate` to `false` and `extend_mintaka` to `true` to finalize the extension of the dataset. 
Reminder: Remember to have installed all the dependencies before running the script. 
   
