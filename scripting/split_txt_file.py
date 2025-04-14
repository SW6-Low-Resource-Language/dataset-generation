from shared_utils.file_service import open_txt, write_txt
import os

def split_txt_file(input_file):
    lines = open_txt(input_file)

    lines_amount = len(lines)
    txt1 = lines[:lines_amount//2]
    txt2 = lines[lines_amount//2:]
    write_txt(txt1, f'{input_file}_1.txt')
    write_txt(txt2, f'{input_file}_2.txt')

def combine_txt_files(file1, file2, output_file):
    lines1 = open_txt(file1)
    lines2 = open_txt(file2)
    combined_lines = lines1 + lines2
    write_txt(combined_lines, output_file)
