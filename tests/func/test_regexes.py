import pytest
from sdsparser.regexes import *


@pytest.mark.regexes
class TestRegexes:

    @pytest.mark.int
    @pytest.mark.parametrize('manufacturer_name, request_keys, expected', [
                            ('sigma_aldrich', ['flash_point'], ['flash_point']),
                            ('firmenich', ['manufacturer', 'specific_gravity'], ['manufacturer', 'specific_gravity']),
                            ('ungerer', None, None)
    ])
    def test_get_regexes(self, manufacturer_name, request_keys, expected):
        regexes = get_static_regexes(manufacturer_name=manufacturer_name, request_keys=request_keys)
        if request_keys is not None:
            assert sorted(expected) == sorted(list(regexes))
        else:
            assert regexes

    ### calc_re_flag
    @pytest.mark.parametrize('flag_string, expected', [
                            ('is', 18),
                            ('lx', 68),
                            ('am', 264)
    ])
    def test_calc_re_flag(self, flag_string, expected):
        assert calc_re_flag(flag_string) == expected

    ### compile_regexes
    def test_compile_regexes(self, ):
        pass

    ### get_manufacturer_name
    def test_get_manufacturer_name(self, ):
        pass

    ### get_manufacturer_regexes
    def test_get_manufacturer_regexes(self, ):
        pass

    ### search_sds_text
    def test_search_sds_text(self, ):
        pass

    ### find_match
    def test_find_match(self, ):
        pass

    ### get_match_string
    def test_get_match_string(self, ):
        pass

    ### filter_dict
    @pytest.mark.parametrize('regex_dict, request_keys, expected',
                            (''))
    def test_filter_dict(self, regex_dict, request_keys, expected):
        pass
