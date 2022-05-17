from pdfminer.high_level import extract_text
import tkinter as tk
from tkinter import filedialog
import re
from pymongo import MongoClient 
import gridfs
import base64

def cv_parser(file_path):
    cluster = MongoClient("mongodb+srv://manu:Rotem889@youtube-articles-api.rjqtk.mongodb.net/?retryWrites=true&w=majority")
    db = cluster['Details-Candidates']
    collection = db['Candidates']
    fs = gridfs.GridFS(db)
    
    with open('cv.txt', 'w', encoding='utf-8') as f:
        f.write(extract_text(file_path))

    with open('cv.txt',  encoding='utf-8') as f:
        lines = f.readlines()
        phone = email = linkedin = id = None
        for line in lines:
            if re.search(r'05[0123456789](\-)?(\s)?(\d{7}|\d{3}(\-)?(\s)?\d{4})', line):
                phone_hanlder = re.search(r'05[0123456789](\-)?(\s)?(\d{7}|\d{3}(\-)?(\s)?\d{4})', line)
                phone = phone_hanlder.group(0)
                print(phone)
            elif re.search(r'\+972(\-)?(\s)?5[0123456789](\-)?(\s)?(\d{7}|\d{3}(\-)?(\s)?\d{4})', line):
                phone_hanlder = re.search(r'\+972(\-)?(\s)?5[0123456789](\-)?(\s)?(\d{7}|\d{3}(\-)?(\s)?\d{4})', line)
                phone = phone_hanlder.group(0)
                print(phone)
            if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', line):
                email_hanlder = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', line)
                email = email_hanlder.group(0)
                print(email)
            if re.search(r'http(s)?:\/\/([\w]+\.)?linkedin\.com\/in\/[A-z0-9_-]+\/?', line):
                linkedin_hanlder = re.search(r'http(s)?:\/\/([\w]+\.)?linkedin\.com\/in\/[A-z0-9_-]+\/?', line)
                linkedin = linkedin_hanlder.group(0) 
                print(linkedin)
            if re.search(r'^[0-9]{9}$', line):
                id_handler = re.search(r'^[0-9]{9}$', line)
                id = id_handler.group(0)
                print(id)
        
        with open(file_path, "rb") as f:
            encoded_string = base64.b64encode(f.read())
        with fs.new_file(
            Email=email,
            Phone_Number=phone,
            LinkedIn = linkedin,
            id=id,
            chunkSize=800000,
            rawDara=file_path) as fp:
            fp.write(encoded_string)

    

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    cv_parser(file_path)