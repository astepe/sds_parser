import os
import re
from PyPDF2 import PdfFileReader
import pdf2image
from PIL import Image
import pytesseract
import zlib


def get_pdf_text(file_path):

    text = ''

    with open(file_path, "rb") as _:
        pdf = PdfFileReader(_, 'rb')
        for page_num in range(pdf.getNumPages()):
            # TODO: unknown error from certain files
            try:
                text += pdf.getPage(page_num).extractText()
            except zlib.error:
                print('data corrupted')
                break
    return text


sds_folder_path = os.path.join(os.getcwd(), 'sds_pdf_files')

company_name_regex = re.compile(r"(s\s*?i\s*?g\s*?m\s*?a\s[\-\s]*?a\s*?l\s*?d\s*?r\s*?i\s*?c\s*?h|p\s*?e\s*?p\s*?s\s*?i\s*?c\s*?o\s*?i\s*?n\s*?c\.?|u\s*?n\s*?g\s*?e\s*?r\s*?e\s*?r|t\s*?a\s*?k\s*?a\s*?s\s*?a\s*?g\s*?o|d\s*?o\s*?e\s*?h\s*?l\s*?e\s*?r|f\s*?r\s*?u\s*?t\s*?a\s*?r\s*?o\s*?m|k\s*?e\s*?r\s*?r\s*?y|f\s*?i\s*?r\s*?m\s*?e\s*?n\s*?i\s*?c\s*?h|s\s*?y\s*?m\s*?r\s*?i\s*?s\s*?e|g\s*?i\s*?v\s*?a\s*?u\s*?d\s*?a\s*?n|r\s*?o\s*?b\s*?e\s*?r\s*?t\s*?e\s*?t|t\s*?r\s*?e\s*?a\s*?t\s*?t|c\s*?i\s*?t\s*?r\s*?u\s*?s\s+?a\s*?n\s*?d\s+?a\s*?l\s*?l\s*?i\s*?e\s*?d|\bi\s*?f\s*?f\b|e\s*?x\s*?c\s*?e\s*?l\s*?l\s*?e\s*?n\s*?t\s*?i\s*?a)", re.I)

for idx, path in enumerate(os.listdir(sds_folder_path)):
    print('-------------------------------------------------------')

    sds_path = os.path.join(sds_folder_path, path)
    print(path)

    text = get_pdf_text(sds_path)

    company_name = company_name_regex.search(text)

    if company_name:
        print(company_name[0].lower())
    # else:
    #     with open(path.split('.')[0] + '.txt', 'w') as text_file:
    #         text_file.write(text)

    print('\n')


# if False:
#     pages = pdf2image.convert_from_path(sds_path, 500)
#
#     image_folder_name = path.split('.')[0]
#     image_folder_full_path = os.path.join(os.getcwd(), 'sds_images', image_folder_name)
#     for idx, page in enumerate(pages):
#         if not os.path.exists(image_folder_full_path):
#             os.mkdir(image_folder_full_path)
#             image_file_full_path = image_folder_full_path + f'/page_{idx+1}.jpg'
#             page.save(image_file_full_path, 'JPEG')
#
#     image_folder = os.listdir(image_folder_full_path)
#
#     for image in image_folder:
#         image_path = os.path.join(image_folder_full_path, image)
#
#         text += pytesseract.image_to_string(Image.open(image_path))
