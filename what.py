from scripting.analysis_of_missing_labels import run_analysis
data_sheets = {
    "dev" : "./data/mintaka_dev.json",
    "test" : "./data/mintaka_test.json",
    "train" : "./data/mintaka_train.json"
}
run_analysis(data_sheets)