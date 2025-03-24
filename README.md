# Purpose

The purpose of this library is to generate the question answer pairs for low-resource languages on the basis of the [Mintaka Dataset](https://github.com/amazon-science/mintaka). 


## Process
The process of generating the dataset consists of:
- Translating the orginial English question to the language of our choice
- Extending the answer label with the label in our target language


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
- Note: For google translation ADC needs to be configured 