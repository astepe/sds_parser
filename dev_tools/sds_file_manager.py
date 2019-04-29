import os
import re
from dev_tools.configs import Configs
from sdsparser import SDSParser
from sdsparser.configs import Configs as PConfigs
from itertools import count
from configs import MongoServer
from errors import SDSDirectoryInvalidName


def check_valid_dir_name(dir_name):
    if dir_name not in PConfigs.SUPPORTED_MANUFACTURERS:
        raise SDSDirectoryInvalidName(dir_name)


def update_sds_pool():
    for sds_directory, _, file_names in os.walk(Configs.SDS_PDF_DIRECTORY):
        if file_names:
            check_valid_dir_name(os.path.split(sds_directory)[1])
            update_sds_file_names(sds_directory, file_names)

            update_txt_files(sds_directory)


def update_sds_file_names(root, file_names):
    parent_dir_name = os.path.split(root)[1]
    for file_name in file_names:
        if not name_is_formatted(parent_dir_name, file_name):

            old_file_path = os.path.join(root, file_name)
            new_file_path = create_unique_file_path(old_file_path)

            os.rename(old_file_path, new_file_path)


def update_txt_files(sds_directory):

    txt_file_set = generate_txt_set()

    for sds_file_name in os.listdir(sds_directory):

        file_root = os.path.splitext(sds_file_name)[0]
        if file_root not in txt_file_set:
            parser = SDSParser()
            parser.get_sds_data(os.path.join(sds_directory, sds_file_name))
            txt_path = generate_txt_file_path(sds_file_name,
                                              ocr=parser.ocr_ran)
            write_text_to_file(parser.sds_text, txt_path)


def name_is_formatted(parent_dir_name, full_file_name, sds_file=True):

    if sds_file:
        raw = Configs.SDS_FILE_NAME.format(manu_key=parent_dir_name)
    else:
        raw = Configs.TXT_FILE_NAME.format(manu_key=parent_dir_name)

    regex = re.compile(raw)

    file_name, _ = os.path.splitext(full_file_name)

    if regex.match(file_name) is not None:
        return True

    return False


# find file names that dont match format
# rename those files accordingly
def create_unique_file_path(old_file_path):
    root, old_file_name = os.path.split(old_file_path)
    ext = os.path.splitext(old_file_name)[1]
    new_name_base = os.path.split(root)[1] + '_'
    counter = count(start=1)
    while True:
        new_file_name = new_name_base + str(next(counter)) + ext
        new_file_path = os.path.join(root, new_file_name)
        if not os.path.exists(new_file_path):
            return new_file_path


def generate_txt_set():
    txt_keys = set()
    for root, dir, files in os.walk(Configs.SDS_TEXT_DIRECTORY):
        if files:
            txt_keys.update({'_'.join(f.split('_')[:-1]) for f in files})
    return txt_keys


def generate_txt_file_path(sds_file_name, ocr=False):
    if ocr:
        extract_type = '_ocr'
    else:
        extract_type = '_pdf'

    text_file_name = os.path.splitext(sds_file_name)[0] + extract_type + '.txt'

    manufacturer_directory = '_'.join(sds_file_name.split('_')[:-1])

    text_file_path = os.path.join(Configs.SDS_TEXT_DIRECTORY,
                                  manufacturer_directory,
                                  text_file_name)

    return text_file_path


def write_text_to_file(sds_text, txt_path):

    root = os.path.split(txt_path)[0]

    if not os.path.exists(root):
        os.mkdir(root)

    with open(txt_path, 'w') as text_file:

        text_file.write(sds_text)


def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


if __name__ == '__main__':
    with MongoServer():
        update_sds_pool()
