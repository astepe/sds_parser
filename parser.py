import os
import re
import csv
from PyPDF2 import PdfFileReader

path = os.getcwd() + "/sds_pdf_files/"
directory = os.fsencode(path)
flash_point = re.compile(r"[F|f]lash [P|p]oint[^a-bd-zA-BD-Z]*?([0-9][^C]*?F)", re.DOTALL)
specific_gravity = re.compile(r"[R|r]elative [D|d]ensity(.){50}", re.DOTALL)
cas_num = re.compile(r"CAS(.){50}", re.DOTALL)

with open('data.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Filename", "Flash Point", "Specific Gravity", "CAS #"])
    for file in os.listdir(directory):
        filename = path + os.fsdecode(file)
        if filename.endswith(".pdf"):
            csv_row = [filename.split('/')[-1].split('.')[0]]
            input_file = PdfFileReader(open(filename, "rb"))
            text = ''
            for page_num in range(input_file.getNumPages()):
                try:
                    text += input_file.getPage(page_num).extractText()
                except:
                    pass

            text = ''.join(text.split('\n'))

            flash = flash_point.search(text)
            spec = specific_gravity.search(text)
            cas = cas_num.search(text)

            if flash:
                csv_row.append(flash.group(1))
            else:
                csv_row.append('None Found')
            if spec:
                csv_row.append(spec[0])
            else:
                csv_row.append('None Found')
            if cas:
                csv_row.append(cas[0])
            else:
                csv_row.append('None Found')

            writer.writerow(csv_row)
