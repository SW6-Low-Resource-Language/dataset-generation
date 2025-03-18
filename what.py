from Services.file_service import open_txt, write_txt
data_sheets = {
    "dev" : "./data/mintaka_dev.json",
    "test" : "./data/mintaka_test.json",
    "train" : "./data/mintaka_train.json"
}


arr = open_txt("./outputs/translations/google/test_questions_bn_linebyline_3.txt")
count = 0
for e in arr:
    if len(e) < 2:
        count += 1
        arr.remove(e)
    print(e)
    print(len(e))
write_txt(arr, "./outputs/translations/google/test_questions_bn_linebyline_4.txt")
print(f"count: {count}")
print(len(arr))
   