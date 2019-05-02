import re
import io
import os
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage, PDFTextExtractionNotAllowed
from pdf2image import convert_from_path
from pytesseract import image_to_string
from PIL import Image
from tqdm import tqdm
import tempfile
from threading import Thread
from .errors import FileMatchNotFound, TextDirectoryDoesNotExist


def get_pdf_image_text(sds_file_path):
    """
    extract text from pdf file by applying ocr
    """

    def get_sorted_dir_list(path):
        """
        mainatain pdf page order after pdf to image conversion
        """

        dir_list = os.listdir(path)
        regex = re.compile(r"[\d]*(?=\.jpg)")
        dir_list.sort(key=lambda x: regex.search(x)[0])
        return dir_list

    def ocr_task(_temp_path):
        nonlocal sds_text
        sds_text += image_to_string(Image.open(_temp_path))

    with tempfile.TemporaryDirectory() as path:

        sds_text = ''

        page_images = convert_from_path(sds_file_path,
                                        fmt='jpeg',
                                        output_folder=path,
                                        dpi=300)

        for i, image in enumerate(page_images):
            page_images[i] = image.convert('L')

        # when converting pdf pages to images, the image files are not
        # output in order
        dir_list = get_sorted_dir_list(path)

        # send each OCR process to a separate thread
        threads = []
        for page_num, page_image in enumerate(dir_list):

            _temp_path = os.path.join(path, page_image)
            thread = Thread(target=ocr_task, args=(_temp_path,))
            _name = f'page {page_num+1} of {os.path.basename(sds_file_path)}'
            thread.setName(_name)
            threads.append(thread)

        for thread in threads:
            thread.start()

        pbar = tqdm(threads, position=1, leave=False)
        for thread in pbar:
            pbar.set_description(f'Applying OCR to {thread.name}')
            thread.join()
        pbar.close()

        return sds_text


def get_pdf_text(sds_file_path):
    """
    extract text directly from pdf file
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

    converter.close()
    fake_file_handle.close()

    return text
