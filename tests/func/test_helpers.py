import pytest
from sdsparser.helpers import *
from random import choice, randint, shuffle
from string import ascii_letters
import os
from tempfile import TemporaryDirectory


class TestConfigs:

    _test_base = os.path.join(os.getcwd())
    TEST_SDS_PDF_DIRECTORY = os.path.join(_test_base, 'test_sds_pdf_files')
    TEST_SDS_TEXT_DIRECTORY = os.path.join(_test_base, 'test_sds_text_files')


@pytest.mark.helpers
class TestHelpers:

    ### fixtures
    def get_file_text(self, file_name):

        text_file = os.path.join(TestConfigs.TEST_SDS_TEXT_DIRECTORY, file_name)

        with open(text_file, 'r') as t:
            text = t.read()

        return text


    @pytest.fixture(scope='module')
    def sig_text(self):

        return self.get_file_text('sigma_aldrich_10_pdf.txt')


    @pytest.fixture(scope='module')
    def sig_file_path(self):
        yield os.path.join(TestConfigs.TEST_SDS_PDF_DIRECTORY, 'sigma_aldrich_10.pdf')



    ### tests
    def test_get_pdf_text(self, sig_file_path, sig_text):
        extracted_text = get_pdf_text(sig_file_path)
        assert extracted_text == sig_text


    # TODO: How to test this effectively?
    # ### get_pdf_image_text
    # def test_get_pdf_image_test(self, sds_file_path):
