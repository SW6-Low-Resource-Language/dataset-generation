
import json


def amountChars(questions):
    char_count = 0
    for question in questions:
        char_count += len(question)
    return char_count


# 112754