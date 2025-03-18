from openpyxl import Workbook 




def generateSheet(mention_ent_obj, output_path):
    wb = Workbook()
    
    for d_name, missing_entities in mention_ent_obj.items():
        ws = wb.create_sheet(title=d_name)
        ws.append(["ID", "Question", "Mention", "Entity", "Category", "Complexity"])
        for id, obj in missing_entities.items():
            if obj["entity"] == None:
                obj["entity"] = "None"
            ws.append([id, obj["question"], obj["mention"], obj["entity"], obj["category"], obj["complexity"]])
    wb.save(output_path)
    print(f"Sheet has been generated at {output_path}")
    



