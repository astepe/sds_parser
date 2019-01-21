import re
import os
import csv
import io
import argparse
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage, PDFTextExtractionNotAllowed
from collections import namedtuple
from pdf2image import convert_from_path
from pytesseract import image_to_string
from PIL import Image
import progressbar
import tempfile
from configs import SDSRegexes, Configs


class SDSParser:

    def __init__(self, request_keys=None):
        """
        define a set of data request keys
        """

        if request_keys is not None:
            self.request_keys = request_keys
        else:
            self.request_keys = SDSRegexes.REQUEST_KEYS

        # determines if ocr will be run
        #self.ocr = False

        # if set to True, program will run ocr if no text
        # or no matches found
        #self.ocr_override = True

    def get_sds_data(self, sds_file_path, **kwargs):
        """
        retrieve requested sds data
        """
        self.ocr = False
        self.ocr_override = True
        if 'ocr' in kwargs:
            self.ocr = kwargs['ocr']
            self.ocr_override = False

        self.sds_text = self.get_sds_text(sds_file_path)

        manufacturer = self.get_manufacturer(self.sds_text)

        if manufacturer is not None:
            regexes = SDSParser.compile_regexes(SDSRegexes.SDS_FORMAT_REGEXES[manufacturer])
        else:
            manufacturer = 'unknown'
            regexes = SDSParser.compile_regexes(SDSRegexes.DEFAULT_SDS_FORMAT)

        sds_data = self.search_sds_text(self.sds_text, regexes)

        data_not_listed = SDSParser.check_empty_matches(sds_data)
        sds_data['format'] = manufacturer
        sds_data['filename'] = sds_file_path.split('/')[-1]
        if data_not_listed and not self.ocr and self.ocr_override:
            print(f'No matches found in {sds_file_path}. Performing ocr...')
            sds_data = self.get_sds_data(sds_file_path, ocr=True)
        return sds_data

    def search_sds_text(self, sds_text, regexes):
        """
        construct a dictionary by iterating over each data request and
        performing a regular expression match
        """

        sds_data = {}

        for request_key in self.request_keys:

            if request_key in regexes:

                title = SDSRegexes.SDS_DATA_TITLES[request_key]
                regex = regexes[request_key]
                match = SDSParser.find_match(sds_text, regex)

                if request_key == 'manufacturer':
                    sds_data[title] = match.lower().title()
                else:
                    sds_data[title] = match

        return sds_data

    @staticmethod
    def check_empty_matches(sds_data):
        """
        check if data not listed
        """

        for _, data in sds_data.items():
            if data.lower() != 'data not listed':
                return False
        return True

    @staticmethod
    def find_match(sds_text, regex):
        """
        perform a regular expression match and return matched data
        """

        match = regex.search(sds_text)

        if match is not None:

            match_string = ''
            group_matches = 0
            for name, group in match.groupdict().items():
                if group is not None:
                    group = group.replace('\n', '').strip()
                    if group_matches > 0:
                        match_string += ', ' + group
                    else:
                        match_string += group
                    group_matches += 1

            if match_string:
                return match_string
            else:
                return 'No data available'

        else:

            return 'Data not listed'

    @staticmethod
    def get_manufacturer(sds_text):
        """
        define set of regular expressions to be used for data matching by searching
        for the manufacturer name within the sds text
        """

        for manufacturer, regexes in SDSRegexes.SDS_FORMAT_REGEXES.items():

            regex = re.compile(*regexes['manufacturer'])

            match = regex.search(sds_text)

            if match:
                print(f'using {manufacturer} format')
                return manufacturer

        print('using default sds format')
        return 'unknown'

    @staticmethod
    def compile_regexes(regexes):
        """
        return a dictionary of compiled regular expressions
        """

        compiled_regexes = {}

        for name, regex in regexes.items():

            compiled_regexes[name] = re.compile(*regex)

        return compiled_regexes

    def get_sds_text(self, sds_file_path):

        if self.ocr is True:
            sds_text = SDSParser.get_sds_image_text(sds_file_path)
        else:
            sds_text = SDSParser.get_sds_pdf_text(sds_file_path)
            if sds_text == '' and self.ocr_override:
                print(f'No text found in {sds_file_path}. Performing ocr...')
                sds_text = SDSParser.get_sds_image_text(sds_file_path)
                self.ocr = True
        return sds_text

    @staticmethod
    def get_sds_pdf_text(sds_file_path):
        """
        extracts text directly from pdf file
        """
        text = ''
        resource_manager = PDFResourceManager()
        fake_file_handle = io.StringIO()
        converter = TextConverter(resource_manager, fake_file_handle)
        page_interpreter = PDFPageInterpreter(resource_manager, converter)
        try:
            with open(sds_file_path, 'rb') as fh:
                for page in PDFPage.get_pages(fh,
                                              caching=True,
                                              check_extractable=True):
                    page_interpreter.process_page(page)

                text = fake_file_handle.getvalue()
        except PDFTextExtractionNotAllowed:
            pass
        # close open handles
        converter.close()
        fake_file_handle.close()

        return text

    @staticmethod
    def get_sds_image_text(sds_file_path):
        """
        converts each pdf page to an image and performs ocr to extract text
        """
        print('=======================================================')
        print('Processing:', sds_file_path.split('/')[-1] + '...')

        with tempfile.TemporaryDirectory() as path:

            page_images = convert_from_path(sds_file_path, fmt='jpeg', output_folder=path, dpi=350)
            dir_list = os.listdir(path)

            # sort path list
            regex = re.compile(r"[\d]*(?=\.jpg)")
            dir_list.sort(key=lambda x: regex.search(x)[0])

            # initialize progress bar
            p_bar = progressbar.ProgressBar().start()
            p_bar_increment = len(dir_list)

            sds_image_text = ''
            for idx, page_image in enumerate(dir_list):

                _temp_path = os.path.join(path, page_image)
                sds_image_text += image_to_string(Image.open(_temp_path))
                p_bar.update((idx/p_bar_increment)*100)

            p_bar.update(100)
            print()
            return sds_image_text


if __name__ == '__main__':

    def is_requested(manufacturer_requests, file_name):
        for request in manufacturer_requests:
            if file.startswith(request):
                return True
        return False

    def get_manu_requests(args):
        manufacturer_requests = []
        for arg in vars(args):
            if getattr(args, arg):
                manufacturer_requests.append(arg)
        return manufacturer_requests

    def generate_manu_args():
        arg_parser = argparse.ArgumentParser(description='select vendors to extract data')
        for manufacturer, _ in SDSRegexes.SDS_FORMAT_REGEXES.items():
            flag = '--' + manufacturer
            arg_parser.add_argument(flag, action='store_true', help=f'extract chemical data from all {manufacturer} SDS files')
        return arg_parser.parse_args()

    sds_parser = SDSParser()
    # set arguments
    args = generate_manu_args()
    # get requested manufacturers
    manufacturer_requests = get_manu_requests(args)

    with open('chemical_data.csv', 'w') as _:
        writer = csv.writer(_)
        writer.writerow([SDSRegexes.SDS_DATA_TITLES[key] for key in sds_parser.request_keys])

        for file in os.listdir(Configs.SDS_PDF_FOLDER):
            if manufacturer_requests:
                if not is_requested(manufacturer_requests, file):
                    continue
            file_path = os.path.join(Configs.SDS_PDF_FOLDER, file)
            chemical_data = sds_parser.get_sds_data(file_path, ocr=False)
            writer.writerow([data for category, data in chemical_data.items()])
