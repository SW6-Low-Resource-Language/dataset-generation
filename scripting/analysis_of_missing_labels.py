from Services.file_service import open_json, write_json


def run_analysis(data_sheets):
    results = {}
    results["all"] = {}
    for data_name, data_path in data_sheets.items():
        results[data_name] = {}
        results[data_name]["total"] = 0
        
        data = open_json(data_path)
        for entry in data:

            # print(entry)
            cat = entry["category"]
            complexity = entry["complexityType"]
            answer = entry["answer"]
            answerType = answer["answerType"]
            if answerType == "entity" and answer["answer"] == None: 

                results[data_name]["total"] += 1
                if cat not in results["all"]:
                    results["all"][cat] = {"total": 0}
                if complexity not in results["all"][cat]:
                    results["all"][cat][complexity] = 0


                if cat not in results[data_name]:
                    results[data_name][cat] = {}
                

                
                if complexity not in results[data_name][cat]:
                    results[data_name][cat][complexity] = 0
                results[data_name][cat][complexity] += 1
                results["all"][cat][complexity] += 1
                results["all"][cat]["total"] += 1
                
            
    write_json(results, "./outputs/missing_labels.json")
   