import argparse
from sdsparser.parser import SDSParser
from sdsparser.configs import Configs
import csv
import os
import pprint
import sys


def main(passed_args=None):
    args = get_args(passed_args)

    request_keys = get_request_keys(args)

    if args.txt_dir is not None:
        sds_txt_dir = args.txt_dir
    else:
        sds_txt_dir = ''

    if args.sds_dir is not None:
        sds_dir = args.sds_dir
    else:
        sds_dir = os.getcwd()

    sds_parser = SDSParser(request_keys=request_keys,
                           file_info=args.file_info)

    sds_data = dict()

    if args.file_name:
        file_path = os.path.join(sds_dir, args.file_name)
        sds_data[args.file_name] = sds_parser.get_sds_data(file_path)
    else:
        for file in os.listdir(sds_dir):
            if file.endswith('.pdf'):

                file_path = os.path.join(sds_dir, file)
                sds_data[file] = sds_parser.get_sds_data(file_path)

    if args.as_dict:
        return sds_data

    if args.csv:

        with open('sds_data.csv', 'w') as _:
            writer = csv.writer(_)
            writer.writerow(list(list(sds_data.values())[0].keys()))

            for _, dict_row in sds_data.items():
                row = list(dict_row.values())
                writer.writerow(row)
    else:
        pp = pprint.PrettyPrinter(width=80, indent=1)
        pp.pprint(sds_data)


def get_request_keys(args_list):

    request_keys = []
    for arg in vars(args_list):
        if arg in Configs.REQUEST_KEYS and getattr(args_list, arg):
            request_keys.append(arg)
    return request_keys


def get_args(passed_args):
    arg_parser = argparse.ArgumentParser(description='select request keys to extract data')

    subparsers = arg_parser.add_subparsers()

    parse_parser = subparsers.add_parser('parse', help='extract sds data from sds documents')

    request_key_flags = ['--' + r for r in Configs.REQUEST_KEYS]

    for flag in request_key_flags:
        request_key = flag[2:]
        parse_parser.add_argument(flag, action='store_true', help=f'extract {request_key}')

    parse_parser.add_argument('-f', '--file_name', type=str, help='extract chemical data from a specific file')

    parse_parser.add_argument('--txt_dir', type=str)

    parse_parser.add_argument('--sds_dir', type=str)

    parse_parser.add_argument('--file_info', action='store_true')

    parse_parser.add_argument('--csv', action='store_true', help='output data to csv file')

    parse_parser.add_argument('--as_dict', action='store_true', help='return values as a python dictionary')

    if len(sys.argv) == 1 and passed_args is None:
        arg_parser.print_help(sys.stderr)
        sys.exit(1)

    if passed_args is not None:
        args = arg_parser.parse_args(passed_args)
    else:
        args = arg_parser.parse_args()
    return args


if __name__ == '__main__':
    main()
