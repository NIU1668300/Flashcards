
import csv
import pdfplumber
import re
import os

csv_path = 'Test/Out/csv_test.csv'
txt_path = 'Resources/tt.txt'
pdf_path = 'Resources/Parcial1.pdf'



def pdf_to_txt(pdf_path,txt_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()

    with open(txt_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for line in text.split('\n'):
            writer.writerow([line])



def extract_questions_and_options(text):
    questions_and_options = []
    
    pattern = re.compile(r'\d+\.- (.*?)\n(a\)) (.*?)\n(b\)) (.*?)\n(c\)) (.*?)\n(d\)) (.*?)(\n|$)')
    matches = pattern.findall(text)
    
    for match in matches:
        question = match[0].strip()
        options = [match[i].strip() for i in range(2, 9, 2)]
        questions_and_options.append([question] + options + [''])  

    return questions_and_options

def write_to_csv(data, csv_path):
    with open(csv_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Question', 'Option1', 'Option2', 'Option3', 'Option4', 'CorrectAnswer'])
        writer.writerows(data)

with open(txt_path, 'r', encoding='utf-8') as file:
    content = file.read()

questions_and_options = extract_questions_and_options(content)

os.remove(txt_path) 
write_to_csv(questions_and_options, csv_path)
print("Succesfully executed")

