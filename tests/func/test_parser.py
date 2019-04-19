import pytest
from sdsparser.parser import SDSParser
from configs import TestConfigs
import os
import re

@pytest.mark.parser
class TestSDSParser:

    @pytest.fixture(scope='module')
    def parser_obj(self):
        yield SDSParser()

    @pytest.fixture(scope='module')
    def iff_file_path(self):
        yield os.path.join(TestConfigs.TEST_SDS_PDF_DIRECTORY, 'firmenich_1.pdf')

    @pytest.fixture(scope='module')
    def iff_image_text(self):
        yield self.get_file_text('firmenich_1_ocr.txt')

    @pytest.fixture(scope='module')
    def sig_file_path(self):
        yield os.path.join(TestConfigs.TEST_SDS_PDF_DIRECTORY, 'sigma_aldrich_10.pdf')

    def get_file_text(self, file_name):

        text_file = os.path.join(TestConfigs.TEST_SDS_TEXT_DIRECTORY, file_name)

        with open(text_file, 'r') as t:
            text = t.read()

        return text

    @pytest.fixture(scope='module')
    def sig_text(self):

        return self.get_file_text('sigma_aldrich_10_pdf.txt')

    # @pytest.fixture(scope='module')
    # def sig_regexes(self):
    #     regexes = SDSRegexes.SDS_FORMAT_REGEXES['sigma_aldrich']
    #     return regexes
    #
    # @pytest.fixture(scope='module')
    # def all_regexes(self):
    #     regexes = SDSRegexes.SDS_FORMAT_REGEXES
    #     yield regexes

    def test_data_not_listed(self, parser_obj):
        parser_obj.sds_data = {'test': 'data not listed',
                               'testing': 'Data not listed'}
        assert parser_obj.data_not_listed()

    @pytest.mark.parametrize("test_input, expected", [
                            ('flash_point', 'No data available'),
                            ('sara_311', 'Chronic Health Hazard')
    ])
    def test_find_match(self, parser_obj, sig_regexes, sig_text, test_input, expected):
        regex = re.compile(*sig_regexes[test_input])
        assert parser_obj.find_match(sig_text, regex) == expected

    def test_compile_regexes(self, parser_obj, sig_regexes):
        regexes = parser_obj.compile_regexes(sig_regexes)
        for name, regex in regexes.items():
            assert isinstance(regex, re.Pattern)

    @pytest.mark.ocr
    def test_get_sds_image_text(self, parser_obj, iff_file_path, iff_image_text):
        extracted_text = parser_obj.get_sds_image_text(iff_file_path)
        assert extracted_text == iff_image_text
