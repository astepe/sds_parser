import os
import json

# support for 3.6
try:
    from importlib.resources import open_binary
except ModuleNotFoundError:
    from pkg_resources import resource_stream as open_binary


class Configs:

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

    REGEXES = dict()

    with open_binary('static', 'regexes.json') as regex_file:
        regex_file_bytes = regex_file.read()

    for regex_dict in json.loads(regex_file_bytes):
        REGEXES[regex_dict['name']] = regex_dict

    SUPPORTED_MANUFACTURERS = set(REGEXES.keys())
    SUPPORTED_MANUFACTURERS.remove('default')
