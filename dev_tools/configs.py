import os
import subprocess


class Configs:

    _sds_pool_base = os.path.join(os.getcwd(), 'sds_pool')

    SDS_PDF_DIRECTORY = os.path.join(_sds_pool_base, 'sds_pdf_files')
    SDS_TEXT_DIRECTORY = os.path.join(_sds_pool_base, 'sds_text_files')

    SDS_FILE_NAME = '{manu_key}_\d+'
    TXT_FILE_NAME = '{manu_key}_{n}_(ocr|pdf))'


class MongoServer:

    def __enter__(self):
        subprocess.run(['sudo', '-S', 'mongod', '--fork', '--quiet', '--logpath', '/home/ari/Desktop/mongo_logs/log.log'])

    def __exit__(self, exc_type, exc_value, traceback):
        subprocess.run(['sudo', 'mongo', '--eval', "db.getSiblingDB('admin').shutdownServer()"])
