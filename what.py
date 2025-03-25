from Services.file_service import open_txt, write_txt
from scripting.split_txt_file import combine_txt_files
data_sheets = {
    "dev" : "./data/mintaka_dev.json",
    "test" : "./data/mintaka_test.json",
    "train" : "./data/mintaka_train.json"
}

input_path = './outputs/translations/deepl/train_questions_da_1.txt'
input_path2 = './outputs/translations/deepl/train_questions_da_2.txt'
output_path = './outputs/translations/deepl/train_questions_da.txt'


combine_txt_files(input_path, input_path2, output_path)