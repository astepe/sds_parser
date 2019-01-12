import re
import os
from PyPDF2 import PdfFileReader, utils
from pdf2image
from PIL import Image
import pytesseract
from collections import namedtuple


class ChemicalData:

    CATEGORY = namedtuple('category', 'name regex')

    CATEGORIES = (
        CATEGORY('Product Name', re.compile(r"[P|p]roduct (([N|n]ame)|([D|d]escription)).*?(?P<data>[^ :\n].*?)(P|C)", re.DOTALL)),
        CATEGORY('Flash Point (°F)', re.compile(r"([F|f]lash [P|p]oint)([\sC\d°:\(.]*?(?P<data>[0-9°.]*)\s*?°?\s?F)?", re.DOTALL)),
        CATEGORY('Specific Gravity', re.compile(r"([R|r]elative [D|d]ensity|[S|s]pecific [G|g]ravity)\s*(?P<data>[0-9.]*\s)?", re.DOTALL)),
        CATEGORY('CAS #', re.compile(r"CAS.*?(?P<data>\d{2,7}\n*?-\n*?\d{2}\n*?-\n*?\d)", re.DOTALL)),
        CATEGORY('NFPA Fire', re.compile(r"NFPA.*?[F|f]ire.*?(?P<data>[0-4])", re.DOTALL)),
        CATEGORY('NFPA Health', re.compile(r"NFPA.*?[H|h]ealth.*?(?P<data>[0-4])", re.DOTALL)),
        CATEGORY('NFPA Reactivity', re.compile(r"NFPA.*?(([R|r]eactivity)|([I|i]nstability)).*?(?P<data>[0-4])", re.DOTALL)),
        CATEGORY('SARA 311/312', re.compile(r"SARA 311.*?(?P<data>(Chronic|Acute|Fire|Reactive)+?(.{0,25}(Hazard|Reactive))+)", re.DOTALL)),
        CATEGORY('Revision Date', re.compile(r"[R|r]evision [D|d]ate.*?(?P<data>\d.*?\s)", re.DOTALL)),
        CATEGORY('Physical State', re.compile(r"F[\s]*?o[\s]*?r[\s]*?m[\s]*?\W(.)*?(?P<data>\w+)\s", re.DOTALL))
        )


def sds_parser():

    file_folder = os.path.join(os.getcwd(), 'sds_pdf_files')

    for sds_file in os.listdir(file_folder):

        pages = pdf2image.convert_from_path(os.path.join(file_folder, sds_file), 500)

        image_folder_name = sds_file.split('.')[0]
        image_folder_full_path = os.path.join(os.getcwd(), 'sds_images', image_folder_name)
        for idx, page in enumerate(pages):
            if not os.path.exists(image_folder_full_path):
                os.mkdir(image_folder_name)
            image_file_full_path = image_folder_full_path + f'/page_{idx+1}.jpg'
            page.save(image_file_full_path, 'JPEG')

        image_folder = os.listdir(image_folder_full_path)

        sds_image_text = ''

        for image in image_folder:
            image_path = os.path.join(image_folder_full_path, image)

            sds_image_text += pytesseract.image_to_string(Image.open(image_path))

        if sds_image_text:

            chemical_data = get_chemical_data(sds_image_text)

            print(chemical_data)


def get_text_from_image(image):
    pass


def get_chemical_data(text):

    chemical_data = []

    for category in ChemicalData.CATEGORIES:

        match_found = category.regex.search(text)

        if match_found:

            if match_found.group('data'):
                match = match_found.group('data').replace('\n', '')
            else:
                match = 'No data available'
            chemical_data.append(match)
            # print(category.name + ': ' + match)

        else:

            chemical_data.append('Category not listed')
            # print(category.name + ': ' + 'Category not listed')

    return chemical_data


def get_pdf_text(file_path):

    text = ''

    with open(file_path, "rb") as _:
        try:
            pdf = PdfFileReader(_, 'rb')
            for page_num in range(pdf.getNumPages()):
                # TODO: unknown error from certain files
                try:
                    text += pdf.getPage(page_num).extractText()
                except:
                    pass
        except utils.PdfReadError:
            print('Pdf EOF not Found')
            return None

    return text


if __name__ == '__main__':
    chemical_data = sds_parser()
