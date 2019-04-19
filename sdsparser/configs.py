import os
import json


class Configs:

    SDS_DEV = os.environ.get('SDS_DEV', False) in ('TRUE', '1')

    REQUEST_KEYS = [
        'manufacturer',
        'product_name',
        'flash_point',
        'specific_gravity',
        'nfpa_fire',
        'nfpa_health',
        'nfpa_reactivity',
        'sara_311',
        'revision_date',
        'physical_state',
        'cas_number',
    ]

    REGEXES_PATH = '/home/ari/Desktop/projects/sdsparser_proj/sdsparser/sdsparser/regexes.json'

    REGEXES = dict()

    with open(REGEXES_PATH, 'r') as json_file:
        for regex_dict in json.load(json_file):
            REGEXES[regex_dict['name']] = regex_dict

    SUPPORTED_MANUFACTURERS = set(REGEXES.keys())
    SUPPORTED_MANUFACTURERS.remove('default')
