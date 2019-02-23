import pytest
from sdsparser import parser, configs
import os
import re


@pytest.fixture(scope='module')
def parser_obj():
    return parser.SDSParser()


@pytest.fixture(scope='module')
def iff_file_path():
    return os.path.join(configs.DevelopmentConfigs.TEST_SDS_PDF_FILES, 'iff_4_ocr.pdf')


@pytest.fixture(scope='module')
def iff_image_text():
    return get_file_text('iff_4_ocr.txt')


@pytest.fixture(scope='module')
def sig_file_path():
    return os.path.join(configs.DevelopmentConfigs.TEST_SDS_PDF_FILES, 'sigma_aldrich_10.pdf')


def get_file_text(file_name):

    text_file = os.path.join(configs.DevelopmentConfigs.TEST_SDS_TEXT_FILES, file_name)

    with open(text_file, 'r') as t:
        text = t.read()

    return text


@pytest.fixture(scope='module')
def sig_text():

    return get_file_text('sigma_aldrich_10_pdf.txt')


@pytest.fixture(scope='module')
def sig_regexes():
    regexes = configs.SDSRegexes.SDS_FORMAT_REGEXES['sigma_aldrich']
    return regexes


@pytest.fixture(scope='module')
def all_regexes():
    regexes = configs.SDSRegexes.SDS_FORMAT_REGEXES
    yield regexes


def test_check_empty_matches(parser_obj):
    assert parser_obj.check_empty_matches({'test': 'data not listed',
                                           'testing': 'data not listed'})


@pytest.mark.parametrize("test_input, expected", [
                        ('flash_point', 'No data available'),
                        ('sara_311', 'Chronic Health Hazard')
])
def test_find_match(parser_obj, sig_regexes, sig_text, test_input, expected):
    regex = re.compile(*sig_regexes[test_input])
    assert parser_obj.find_match(sig_text, regex) == expected


def manufacturer_test_set():
    text_folder = configs.DevelopmentConfigs.TEST_SDS_TEXT_FILES
    text_files = os.listdir(text_folder)
    test_set = []
    for text_file in text_files:
        expected = '_'.join(text_file.split('_')[0:-2])
        text_file_path = os.path.join(configs.DevelopmentConfigs.SDS_TEXT_FILES, text_file)
        with open(text_file_path, 'r') as text:
            test_input = text.read()
        test_set.append((test_input, expected))
    return test_set


@pytest.mark.parametrize('test_input, expected', manufacturer_test_set())
def test_get_manufacturer(parser_obj, test_input, expected):
    assert parser_obj.get_manufacturer(test_input) == expected


def test_compile_regexes(parser_obj, sig_regexes):
    regexes = parser_obj.compile_regexes(sig_regexes)
    for name, regex in regexes.items():
        assert isinstance(regex, re.Pattern)


def test_get_sds_pdf_text(parser_obj, sig_file_path, sig_text):
    extracted_text = parser_obj.get_sds_pdf_text(sig_file_path)
    assert extracted_text == sig_text


@pytest.mark.ocr
def test_get_sds_image_text(parser_obj, iff_file_path, iff_image_text):
    extracted_text = parser_obj.get_sds_image_text(iff_file_path)
    assert extracted_text == iff_image_text
