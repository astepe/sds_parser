import os
import subprocess


class Configs:

    _sds_pool_base = os.path.join(os.getcwd(), 'sds_pool')

    SDS_PDF_DIRECTORY = os.path.join(_sds_pool_base, 'sds_pdf_files')
    SDS_TEXT_DIRECTORY = os.path.join(_sds_pool_base, 'sds_text_files')

    SDS_FILE_NAME = '{manu_key}_\d+'
    TXT_FILE_NAME = '{manu_key}_{n}_(ocr|pdf))'


class MongoServer:

    @staticmethod
    def import_from_static_file():
        subprocess.run(['mongoimport', '--db', 'sdsparser', '--collection', 'sdsRegexes', '--file', '../sdsparser/static/regexes.json', '--jsonArray'])

    def __enter__(self):
        subprocess.run(['sudo', '-S', 'mongod', '--quiet', '--fork', '--logpath', './mongologs/mongolog.log'])
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        subprocess.run(['sudo', 'mongo', '--eval', "db.getSiblingDB('admin').shutdownServer()"])
