from parser import SDSParser, SDSRegexes
import os
import re


def test_extract_text():
    sds_folder = os.getcwd() + '/sds_pdf_files'
    sds_file = os.listdir(sds_folder)
    text = SDSParser.extract_text(sds_file[0])
    assert text is not None


def test_compile_regexes():
    for manufacturer, regexes in SDSRegexes.SDS_FORMAT_REGEXES.iteritems():
        compiled_regexes = SDSParser.compile_regexes(regexes)
        for data_name, regex in compiled_regexes.iteritems():
            assert isinstance(regex, re.Pattern)


class TestSDSParser:

    def test_get_format_regexes():
        
