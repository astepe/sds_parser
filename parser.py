import os
import re
import csv
from PyPDF2 import PdfFileReader


def write_to_csv():

    sds_directory = os.getcwd() + "/sds_pdf_files/"

    with open('data.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Product Name",
                         "Flash Point",
                         "Specific Gravity",
                         "CAS #"
                         ])

        for file in os.listdir(sds_directory):
            file_path = sds_directory + file

            print('---------------------------------------------', end='\n')
            print('file_name: ', file)

            if file_path.endswith(".pdf"):

                raw_text = get_pdf_text(file_path)

                matches = match_fields(raw_text)

                csv_row = [matches['product_name'],
                           matches['flash_point'],
                           matches['specific_gravity'],
                           matches['cas_number']
                           ]

                writer.writerow(csv_row)


def get_pdf_text(file_path):

    text = ''

    with open(file_path, "rb") as _:
        pdf = PdfFileReader(_, 'rb')
        for page_num in range(pdf.getNumPages()):
            try:
                text += pdf.getPage(page_num).extractText()
            except:
                pass
    return text


def match_fields(text):

    product_name = re.compile(r"[P|p]roduct (([N|n]ame)|([D|d]escription)).*?(?P<data>[^ :\n].*?)(P|C)", re.DOTALL)
    flash_point = re.compile(r"[F|f]lash [P|p]oint[^a-bd-zA-BD-Z]*?(?P<data>[0-9][^C]*?F)", re.DOTALL)
    specific_gravity = re.compile(r"([R|r]elative [D|d]ensity|[S|s]pecific [G|g]ravity)\s*?(?P<data>[0-9.]+?\s)", re.DOTALL)
    cas_num = re.compile(r"(?P<data>\d{2,7}\n*?-\n*?\d{2}\n*?-\n*?\d)", re.DOTALL)

    matches = {'product_name': 'Not Found',
               'flash_point': 'Not Found',
               'specific_gravity': 'Not Found',
               'cas_number': 'Not Found',
               }

    product_match = product_name.search(text)
    flash_match = flash_point.search(text)
    spec_match = specific_gravity.search(text)
    cas_match = cas_num.search(text)

    if product_match:
        matches['product_name'] = product_match.group('data').replace('\n', '')
    if flash_match:
        matches['flash_point'] = flash_match.group('data').replace('\n', '')
    if spec_match:
        matches['specific_gravity'] = spec_match.group('data').replace('\n', '')
    if cas_match:
        matches['cas_number'] = cas_match.group('data').replace('\n', '')

    for name, match in matches.items():
        print(name, ' :', match)
    print('\n')

    return matches


if __name__ == '__main__':
    write_to_csv()
