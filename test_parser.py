import pytest
import parser
import configs
import os
import re


@pytest.fixture(scope='module')
def parser_obj():
    return parser.SDSParser()


@pytest.fixture(scope='module')
def sig_text():

    text_file = os.path.join(configs.Configs.SDS_TEXT_FOLDER, 'sigma_aldrich_10_pdf.txt')

    with open(text_file, 'r') as text:
        sig_text = text.read()

    return sig_text


@pytest.fixture(scope='module')
def sig_regexes():
    regexes = configs.SDSRegexes.SDS_FORMAT_REGEXES['sigma_aldrich']
    return regexes


@pytest.fixture(scope='module')
def all_regexes():
    regexes = configs.SDSRegexes.SDS_FORMAT_REGEXES
    yield regexes


def test_extract_text(parser_obj):
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
    text_folder = configs.Configs.SDS_TEST_TEXT_FOLDER
    text_files = os.listdir(text_folder)
    test_set = []
    for text_file in text_files:
        expected = '_'.join(text_file.split('_')[0:-2])
        text_file_path = os.path.join(configs.Configs.SDS_TEXT_FOLDER, text_file)
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
