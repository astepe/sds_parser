import os


class TestConfigs:

    _test_base = os.getcwd()
    TEST_SDS_PDF_DIRECTORY = os.path.join(_test_base, 'test_sds_pdf_files')
    TEST_SDS_TEXT_DIRECTORY = os.path.join(_test_base, 'test_sds_text_files')
