import argparse
from sdsparser.parser import SDSParser
from sdsparser.configs import SDSRegexes
import csv
import os
import pprint


def main():
    args = get_args()

    request_keys = get_request_keys(args)

    sds_parser = SDSParser(request_keys=request_keys)

    sds_data = dict()

    if args.file_name:
        file_path = os.path.join(os.getcwd(), args.file_name)
        sds_data[args.file_name] = sds_parser.get_sds_data(file_path)
    else:
        for file in os.listdir(os.getcwd()):
            if file.endswith('.pdf'):

                file_path = os.path.join(os.getcwd(), file)
                sds_data[file] = sds_parser.get_sds_data(file_path)

    if args.csv:

        with open('sds_data.csv', 'w') as _:
            writer = csv.writer(_)
            writer.writerow(request_keys)

            for _, dict_row in sds_data.items():
                row = list(dict_row.values())
                writer.writerow(row)
    else:
        pp = pprint.PrettyPrinter(width=80, indent=1)
        pp.pprint(sds_data)


def get_request_keys(args_list):

    request_keys = []
    for arg in vars(args_list):
        if arg in SDSRegexes.REQUEST_KEYS and getattr(args_list, arg):
            request_keys.append(arg)
    return request_keys


def get_args():
    arg_parser = argparse.ArgumentParser(description='select request keys to extract data')

    request_key_flags = ['--' + r for r in SDSRegexes.REQUEST_KEYS]

    for flag in request_key_flags:
        request_key = flag[2:]
        arg_parser.add_argument(flag, action='store_true', help=f'extract {request_key}')

    arg_parser.add_argument('-f', '--file_name', type=str, help='extract chemical data from a specific file')

    arg_parser.add_argument('--csv', action='store_true', help='output data to csv file')

    args = arg_parser.parse_args()
    return args


if __name__ == '__main__':
    main()
