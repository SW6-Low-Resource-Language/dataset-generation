
import json

with open("../data/id2question_dev.json", 'r', encoding='utf-8') as f:
        data = json.load(f)

char_count = 0
for key, value in data.items():
    char_count += len(value)

print(f"Der er {char_count} bogstaver i alt i alle spørgsmålene der skal oversættes")
# 112754