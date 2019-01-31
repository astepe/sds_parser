import os
import configs
import parser


def rename_all_sds_files():

    sds_pdf_dir = configs.Configs.SDS_PDF_FILES

    sds_files = os.listdir(sds_pdf_dir)

    for sds_file in sds_files:
        sds_file_path = os.path.join(sds_pdf_dir, sds_file)
        sds_parser = parser.SDSParser(request_keys=['manufacturer'])
        sds_data = sds_parser.get_sds_data(sds_file_path)
        print(sds_data)

        if sds_data:
            num = 1
            format = sds_data['format'].lower()
            new_sds_file_name = format + '_' + str(num) + '.pdf'
            new_sds_file_path = os.path.join(sds_pdf_dir, new_sds_file_name)
            while os.path.exists(new_sds_file_path):
                num += 1
                new_sds_file_name = format + '_' + str(num) + '.pdf'
                new_sds_file_path = os.path.join(sds_pdf_dir, new_sds_file_name)
            os.rename(sds_file_path, new_sds_file_path)
            write_text_to_file(sds_parser.sds_text,
                               new_sds_file_name,
                               ocr=sds_parser.ocr_ran)


def write_text_to_file(sds_text, sds_file_name, ocr=False):

    sds_text_dir = configs.Configs.SDS_TEXT_FILES

    if ocr is True:
        extract_type = '_ocr'
    else:
        extract_type = '_pdf'

    text_file_name = sds_file_name.split('.')[0] + extract_type + '.txt'

    text_file_path = os.path.join(sds_text_dir, text_file_name)

    with open(text_file_path, 'w') as text_file:

        text_file.write(sds_text)


def update_sds_directory():

    sds_pdf_dir = configs.Configs.SDS_PDF_FILES
    sds_text_dir = configs.Configs.SDS_TEXT_FILES

    pdf_files = os.listdir(sds_pdf_dir)
    text_files = os.listdir(sds_text_dir)

    for pdf_file in pdf_files:
        pdf_name = pdf_file.split('.')[0]
        match = False
        for text_file in text_files:
            if text_file.startswith(pdf_name):
                match = True
        if not match:
            print('making new')
            sds_file_path = os.path.join(sds_pdf_dir, pdf_file)
            create_sds_entry(sds_file_path)


def create_sds_entry(sds_file_path):

    sds_pdf_dir = configs.Configs.SDS_PDF_FILES

    sds_parser = parser.SDSParser(request_keys=['manufacturer'])
    sds_data = sds_parser.get_sds_data(sds_file_path)
    print(sds_data)

    if sds_data:
        num = 1
        format = sds_data['format'].lower()
        new_sds_file_name = format + '_' + str(num) + '.pdf'
        new_sds_file_path = os.path.join(sds_pdf_dir, new_sds_file_name)
        while os.path.exists(new_sds_file_path):
            num += 1
            new_sds_file_name = format + '_' + str(num) + '.pdf'
            new_sds_file_path = os.path.join(sds_pdf_dir, new_sds_file_name)
        os.rename(sds_file_path, new_sds_file_path)
        write_text_to_file(sds_parser.sds_text,
                           new_sds_file_name,
                           ocr=sds_parser.ocr_ran)


if __name__ == '__main__':
    update_sds_directory()
