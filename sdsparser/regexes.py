import re
from .configs import Configs
from .errors import ManufacturerNotSupported

"""
Manages regular expression retrieval
"""


def get_static_regexes(manufacturer_name=None, request_keys=None):
    """
    retrieves regular expressions from static regex file and filters based
    on manufacturer_name and request_keys
    :param manufacturer_name: the name of a supported safety data sheet
                              manufacturer
    :param request_keys: used to filter through regex dictionary
    """
    if not isinstance(request_keys, list):
        request_keys = Configs.REQUEST_KEYS

    raw_dict = dict()

    if manufacturer_name is None:

        for name, doc in Configs.REGEXES.items():
            raw_dict.update({name: filter_dict(doc, request_keys)})

    else:

        try:
            regex_dict = Configs.REGEXES[manufacturer_name]
        except KeyError:
            raise ManufacturerNotSupported(manufacturer_name)
            regex_dict = Configs.REGEXES['default']
        finally:
            raw_dict = {manufacturer_name: filter_dict(regex_dict,
                                                       request_keys)}

    out_dict = dict()
    for name, doc in raw_dict.items():
        regexes = dict()

        for key, regex in doc['regexes'].items():
            compiled = compile_regexes({key: regex})
            regexes[key] = compiled[key]

        out_dict[name] = regexes

    return out_dict


def compile_regexes(regexes):
    """
    return a dictionary of compiled regular expressions
    input structure:
    ```
    {
    'flash_point': {
        'regex': 'hello',
        'flags': 'is'
        },
    'manufacturer': {
        'regex': 'hi',
        'flags': 'i'
        }
    }
    returns
    {
    'flash_point': re.Pattern
    'manufacturer': re.Pattern
    }
    ```
    :param regexes: a dictionary mapping regular expression names to raw
                    regular expressions and and relevant flags
    """

    compiled_regexes = {}

    for regex_key, regex_data in regexes.items():
        regex = regex_data['regex']
        flags = calc_re_flag(regex_data['flags'])
        compiled_regexes[regex_key] = re.compile(regex, flags)

    return compiled_regexes


def filter_dict(regex_dict, request_keys):
    """
    filter regular expression dictionary by request_keys
    :param regex_dict: a dictionary of regular expressions that
                       follows the following format:
                   {
                   "name": "sigma_aldrich",
                   "regexes": {
                    "manufacturer": {
                        "regex": "[C|c]ompany(?P\u003cdata\u003e.{80})",
                        "flags": "is"
                        },
                        "product_name": {
                        "regex": "\\s[P|p]roduct\\s(?P\u003cdata\u003e.{80})",
                        "flags": "is"
                        },
                    ...
                    }
                    returns
                    {
                    'sigma_aldrich': {
                        "manufacturer": {
                            "regex": "[C|c]ompany(?P\u003cdata\u003e.{80})",
                            "flags": "is"
                            },
                        }

    :param request_keys: a list of dictionary keys that correspond to valid
                         regex lookups i.e. ['manufacturer', 'product_name']
    """

    out_dict = dict()
    nested_regexes = regex_dict['regexes']

    for request_key in request_keys:
        if request_key in nested_regexes:
            out_dict[request_key] = nested_regexes[request_key]

    return {'name': regex_dict['name'], 'regexes': out_dict}


def get_manufacturer_name(sds_text):
    """
    find the manufacturer_name within the given text
    :param sds_text: safety data sheet text
    """
    static_regexes = get_static_regexes(request_keys=['manufacturer'])
    for name, regex_dict in static_regexes.items():
        if name == 'default':
            continue

        manufacturer_name = name

        regex = regex_dict['manufacturer']

        match = regex.search(sds_text)

        if match:
            return manufacturer_name

    return 'default'


def search_sds_text(sds_text, regexes):
    """
    using the provided regular expressions, return a dictionary of matches
    :param sds_text: safety data sheet text
    :param regexes: a dictionary mapping field names to corresponding
                    pre-compiled regular expressions. Follows format:
                    input
                    {
                    'manufacturer': re.Pattern,
                    'flash_point': re.Pattern
                    }
                    return
                    {
                    'manufacturer': 'Sigma Aldrich',
                    'flash_point': '70 F'
                    }
    """

    sds_data = dict()

    for name, regex in regexes.items():
        match = find_match(sds_text, regex)
        sds_data[name] = match

    return sds_data


def find_match(sds_text, regex):
    """
    perform a regular expression match and return match string
    :param sds_text: safety data sheet text
    :param regex: a pre-compiled re object
    """

    matches = regex.search(sds_text)

    if matches is not None:

        return get_match_string(matches)

    else:

        return 'Data not listed'


def get_match_string(matches):
    """
    collect and return any matched groups that contain data,
    otherwise, return 'No data available'
    :param matches: an re match object
    """

    group_matches = 0
    match_string = ''

    for name, group in matches.groupdict().items():
        if group is not None:

            group = group.replace('\n', '').strip()

            if group_matches > 0:
                match_string += ', ' + group
            else:
                match_string += group

            group_matches += 1

    if not match_string:
        match_string = 'No data available'

    return match_string


def calc_re_flag(flag_string):
    """
    Calculate the re flag by converting from string notation (i.e. 'is') to
    re flag objects (equivalent to (re.I|re.S))
    :param flag_string: a string representation of regular expression flags
                        (i.e. "is" or "mx")
    """

    num = 0
    for flag in flag_string:
        re_flag = getattr(re, flag.upper())
        num |= re_flag
    return num
