import re
import os


class DevelopmentConfigs:

    _sds_pool_base = os.path.join(os.getcwd(), 'dev/sds_pool')
    _test_base = os.path.join(os.getcwd(), 'dev/test')

    SDS_PDF_FILES = os.path.join(_sds_pool_base, 'sds_pdf_files')
    SDS_TEXT_FILES = os.path.join(_sds_pool_base, 'sds_text_files')
    TEST_SDS_PDF_FILES = os.path.join(_test_base, 'test_sds_pdf_files')
    TEST_SDS_TEXT_FILES = os.path.join(_test_base, 'test_sds_text_files')


class SDSRegexes:

    # list of keys used for regex lookup
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

    # SDS_FORMAT_REGEXES is a dict mapping manufacturer names ('Takasago', 'Robertet', etc.)
    # to a dict of regexes specific to the manufacturer SDS format where the keys are data_request_keys
    # and the values are regexes for those specific data searches
    SDS_FORMAT_REGEXES = {

        'citrus_and_allied': {
            'manufacturer': (r"(?P<data>\bcitrus\s*?and\s*?allied\b)", re.I),
            'product_name': (r"chemical\s*?identification[\s:]*(?P<data>.*?)product", (re.S|re.I)),
            'flash_point': (r"flash\s?point.*?(?P<data>\d+)[^c]{3}", (re.S|re.I)),
            'specific_gravity': (r"specific\s*?gravity.*?:.*?(?P<data>[\d.]+)", (re.S|re.I)),
            'cas_number': (r"CAS(?P<data>.{30})", (re.S|re.I)),
            'nfpa_fire': (r"NFPA.*?[F|f]ire.*?(?P<data>[0-4])", (re.S|re.I)),
            'nfpa_health': (r"NFPA.*?[H|h]ealth.*?(?P<data>[0-4])", (re.S|re.I)),
            'nfpa_reactivity': (r"NFPA.*?(([R|r]eactivity)|([I|i]nstability)).*?(?P<data>[0-4])", (re.S|re.I)),
            'sara_311': (r"SARA 311(?P<data>.{80})", (re.S|re.I)),
            'revision_date': (r"revision\s*?date\D*(?P<data>[\d\-\/]{6,15})", (re.S|re.I)),
            'physical_state': (r"appearance.{0,80}(?P<data>(liquid|solid))", (re.S|re.I))
        },
        'excellentia': {
            'manufacturer': (r"(?P<data>\bexcellentia\b)", re.I),
            'product_name': (r"trade\s*?name(\(s\))[\s:]*(?P<data>.*?)(·|article)", (re.S|re.I)),
            'flash_point': (r"flash\s*?point([\sC\d°:\(\).]*?(?P<data>[0-9.]*)\s*?°?\s*?F)?", (re.S|re.I)),
            'specific_gravity': (r"relative\s*?density[:\s]*(?P<data>[\d.]*)", (re.S|re.I)),
            'cas_number': (r"CAS(?P<data>.{30})", (re.S|re.I)),
            'nfpa_fire': (r"nfpa.*?fire\D*(?P<data>\d)", (re.S|re.I)),
            'nfpa_health': (r"nfpa.*?health\D*(?P<data>\d)", (re.S|re.I)),
            'nfpa_reactivity': (r"nfpa.*?reactivity\D*(?P<data>\d)", (re.S|re.I)),
            'sara_311': (r"sara 311(?P<data>.{80})", (re.S|re.I)),
            'revision_date': (r"last\s*?revision\D*(?P<data>[\d\/]*)", (re.S|re.I)),
            'physical_state': (r"appearance.{0,10}form\W*(?P<data>\w*)", (re.S|re.I))
        },
        'firmenich': {
            'manufacturer': (r"(?P<data>\bfirmenich\b)", re.I),
            'product_name': (r"(chemical\s*?name|product)[\s:\d\w\-]*?(?P<data>[^\-\d:]*?)(revised|synonyms)", (re.S|re.I)),
            'flash_point': (r"flash\s*?point.*?((?P<fahrenheit>\d[\d.,\s]*)°?\s*?(\bF\b|Fahrenheit)|(?P<celsius>\d[\d.,\s]*)°?C(?!.{1,50}?(\bF\b|Fahrenheit)))", (re.S|re.I)),
            'specific_gravity': (r"specific\s*?gravity.{1,50}?(?P<data>\d*\.\d*)", (re.S|re.I)),
            'cas_number': (r"CAS(?P<data>.{30})", (re.S|re.I)),
            'nfpa_fire': (r"NFPA.*?[F|f]ire.*?(?P<data>[0-4])", (re.S|re.I)),
            'nfpa_health': (r"NFPA.*?[H|h]ealth.*?(?P<data>[0-4])", (re.S|re.I)),
            'nfpa_reactivity': (r"NFPA.*?(([R|r]eactivity)|([I|i]nstability)).*?(?P<data>[0-4])", (re.S|re.I)),
            'sara_311': (r"SARA 311(?P<data>.{80})", (re.S|re.I)),
            'revision_date': (r"[R|r]evision [D|d]ate(?P<data>.{20})", (re.S|re.I)),
            'physical_state': (r"F[\s]*?o[\s]*?r[\s]*?m[\s]*?\W(?P<data>.{30})", (re.S|re.I))
        },
        'fisher': {
            'manufacturer': (r"(?P<data>\bfisher\b)", re.I),
            'product_name': (r"product\s*name\W*(?P<data>[()\d\-\w\s,+%]*?)(cat\b|stock)", (re.S|re.I)),
            'flash_point': (r"flash\s*point.*?(?P<data>\d*)", (re.S|re.I)),
            'specific_gravity': (r"(relative\s*density|specific\s*gravity)\D*?(?P<data>[\d.]*)", (re.S|re.I)),
            'cas_number': (r"product\s*name.{1,250}[^a-z]cas\b.*?(?P<data>\d{2,7}-\d{2}-\d)", (re.S|re.I)),
            'nfpa_fire': (r"NFPA.{0,1000}?flammability.{0,10}?(?P<data>[0-4]+?)", (re.S|re.I)),
            'nfpa_health': (r"NFPA.{0,1000}?health.{0,10}?(?P<data>[0-4]+?)", (re.S|re.I)),
            'nfpa_reactivity': (r"NFPA.{0,1000}?(reactivity|instability).{0,10}?(?P<data>[0-4]+?)", (re.S|re.I)),
            'sara_311': (r"SARA 311(?P<data>.{80})", (re.S|re.I)),
            'revision_date': (r"revision\s*date\s*?(?P<data>([\d\-\/.,a-z]|\s(?=(\d|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)))*\d)", (re.S|re.I)),
            'physical_state': (r"((P|p)hysical\s*(S|s)tate|\b(F|f)orm\b:?)\s*(?P<data>[A-Z][a-z]*)", (re.S))
        },
        'frutarom': {
            'manufacturer': (r"(?P<data>\bf\s*?r\s*?u\s*?t\s*?a\s*?r\s*?o\s*?m\b)", re.I),
            'product_name': (r"\s[P|p]roduct\s(?P<data>.{80})", (re.S|re.I)),
            'flash_point': (r"[F|f]lash\s*?[P|p]oint(?P<data>.{30})", (re.S|re.I)),
            'specific_gravity': (r"([R|r]elative [D|d]ensity|[S|s]pecific [G|g]ravity)(?P<data>.{30})", (re.S|re.I)),
            'cas_number': (r"CAS(?P<data>.{30})", (re.S|re.I)),
            'nfpa_fire': (r"NFPA.*?[F|f]ire.*?(?P<data>[0-4])", (re.S|re.I)),
            'nfpa_health': (r"NFPA.*?[H|h]ealth.*?(?P<data>[0-4])", (re.S|re.I)),
            'nfpa_reactivity': (r"NFPA.*?(([R|r]eactivity)|([I|i]nstability)).*?(?P<data>[0-4])", (re.S|re.I)),
            'sara_311': (r"SARA 311(?P<data>.{80})", (re.S|re.I)),
            'revision_date': (r"[R|r]evision [D|d]ate(?P<data>.{20})", (re.S|re.I)),
            'physical_state': (r"F[\s]*?o[\s]*?r[\s]*?m[\s]*?\W(?P<data>.{30})", (re.S|re.I))
        },
        'givaudan': {
            'manufacturer': (r"(?P<data>\bgivaudan\b)", re.I),
            'product_name': (r"sales\s*?no\.[:\s\d]*\s*?(?P<data>.*?)relevant", (re.S|re.I)),
            'flash_point': (r"flash\s*?point([\sC\d°:\(.\)]*?(?P<data>[0-9.]*)\s*?°?\s*?F)?", (re.S|re.I)),
            'specific_gravity': (r"(?<!bulk\s)density[\s:]*(?P<data>[\d\W]*)", (re.S|re.I)),
            'cas_number': (r"CAS(?P<data>.{30})", (re.S|re.I)),
            'nfpa_fire': (r"nfpa.*fire.*?(?P<data>\d)", (re.S|re.I)),
            'nfpa_health': (r"nfpa.*fire.*?(?P<data>\d)", (re.S|re.I)),
            'nfpa_reactivity': (r"nfpa.*fire.*?(?P<data>\d)", (re.S|re.I)),
            'sara_311': (r"sara\s*?311.*?((?P<fire>fire hazard\s*)|(?P<acute>acute health hazard\s*)|(?P<chronic>chronic health hazard\s*)|(?P<reactive>reactive hazard\s*)|(?P<sudden>sudden release of pressure\s*))+", (re.S|re.I)),
            'revision_date': (r"revision\s*?date[:\s]*(?P<data>[\d\-\/\w\s]*?)\bp", (re.S|re.I)),
            'physical_state': (r"physical\s*?state[\s:]*(?P<data>[\w]*)", (re.S|re.I))
        },
        'iff': {
            'manufacturer': (r"(?P<data>\biff\b)", re.I),
            'product_name': (r"\sproduct\s*?name[:\s]*(?P<data>.*?)\biff\b", (re.S|re.I)),
            'flash_point': (r"flash\s*?point([\sC\d°:\(.]*?(?P<data>[0-9.]*)\s*?°?\s*?F)?", (re.S|re.I)),
            'specific_gravity': (r"relative\s*?density\s*?.*?:(?P<data>[\d\.\s]*)", (re.S|re.I)),
            'cas_number': (r"CAS(?P<data>.{30})", (re.S|re.I)),
            'nfpa_fire': (r"NFPA.*?[F|f]ire.*?(?P<data>[0-4])", (re.S|re.I)),
            'nfpa_health': (r"NFPA.*?[H|h]ealth.*?(?P<data>[0-4])", (re.S|re.I)),
            'nfpa_reactivity': (r"NFPA.*?(([R|r]eactivity)|([I|i]nstability)).*?(?P<data>[0-4])", (re.S|re.I)),
            'sara_311': (r"sara\s*?311.*?:(?P<data>(\s|fire|hazard|health|acute|chronic)*)", (re.S|re.I)),
            'revision_date': (r"revision\s*?date[\s:]*(?P<data>[\d\/\-\s]*)", (re.S|re.I)),
            'physical_state': (r"physical\s*?state[\s:]*(?P<data>\w*)", (re.S|re.I))
        },
        'kerry': {
            'manufacturer': (r"(?P<data>\bkerry\b)", re.I),
            'product_name': (r"product\s*?name[\s:]*(?P<data>\D*)(\d|product)", (re.S|re.I)),
            'flash_point': (r"flash\s*?point\D*(?P<data>[0-9. °CF]+)", (re.S|re.I)),
            'specific_gravity': (r"relative\s*?density\D*(?P<data>[\d.]+)", (re.S|re.I)),
            'cas_number': (r"CAS(?P<data>.{30})", (re.S|re.I)),
            'nfpa_fire': (r"NFPA.*?[F|f]ire.*?(?P<data>[0-4])", (re.S|re.I)),
            'nfpa_health': (r"NFPA.*?[H|h]ealth.*?(?P<data>[0-4])", (re.S|re.I)),
            'nfpa_reactivity': (r"NFPA.*?(([R|r]eactivity)|([I|i]nstability)).*?(?P<data>[0-4])", (re.S|re.I)),
            'sara_311': (r"SARA 311(?P<data>.{80})", (re.S|re.I)),
            'revision_date': (r"date\s*?of\s*?revision\D*(?P<data>[\d.\-\/]+)", (re.S|re.I)),
            'physical_state': (r"appearance.{0,80}(?P<data>(liquid|solid))", (re.S|re.I))
        },
        'pepsico_inc': {
            'manufacturer': (r"(?P<data>\bpepsico\s*?inc\b)", re.I),
            'product_name': (r"product\s*?name[\s:]*(?P<data>\D*)document", (re.S|re.I)),
            'flash_point': (r"flash\s*point.{1,50}?((?P<farenheit>\d[\d°\s,]+)°\s*?f|(?P<celcius>\d[\d°\s,]+C(?![\d\s\(>,°]{1,50}?f)))", (re.S|re.I)),
            'specific_gravity': (r"specific\s*?gravity\D{0,25}(?P<data>[\d,]*)", (re.S|re.I)),
            'cas_number': (r"CAS(?P<data>.{30})", (re.S|re.I)),
            'nfpa_fire': (r"NFPA.*?[F|f]ire.*?(?P<data>[0-4])", (re.S|re.I)),
            'nfpa_health': (r"NFPA.*?[H|h]ealth.*?(?P<data>[0-4])", (re.S|re.I)),
            'nfpa_reactivity': (r"NFPA.*?(([R|r]eactivity)|([I|i]nstability)).*?(?P<data>[0-4])", (re.S|re.I)),
            'sara_311': (r"SARA 311(?P<data>.{80})", (re.S|re.I)),
            'revision_date': (r"revision\s*?date\D{0,25}(?P<data>\d[\d\-\w]*\d)", (re.S|re.I)),
            'physical_state': (r"physical\s*?state[:\-\s]*(?P<data>\w*)", (re.S|re.I))
        },
        'robertet': {
            'manufacturer': (r"(?P<data>\br\s*?o\s*?b\s*?e\s*?r\s*?t\s*?e\s*?t\b)", re.I),
            'product_name': (r"\s[P|p]roduct\s(?P<data>.{80})", (re.S|re.I)),
            'flash_point': (r"[F|f]lash\s*?[P|p]oint(?P<data>.{30})", (re.S|re.I)),
            'specific_gravity': (r"([R|r]elative [D|d]ensity|[S|s]pecific [G|g]ravity)(?P<data>.{30})", (re.S|re.I)),
            'cas_number': (r"CAS(?P<data>.{30})", (re.S|re.I)),
            'nfpa_fire': (r"NFPA.*?[F|f]ire.*?(?P<data>[0-4])", (re.S|re.I)),
            'nfpa_health': (r"NFPA.*?[H|h]ealth.*?(?P<data>[0-4])", (re.S|re.I)),
            'nfpa_reactivity': (r"NFPA.*?(([R|r]eactivity)|([I|i]nstability)).*?(?P<data>[0-4])", (re.S|re.I)),
            'sara_311': (r"SARA 311(?P<data>.{80})", (re.S|re.I)),
            'revision_date': (r"[R|r]evision [D|d]ate(?P<data>.{20})", (re.S|re.I)),
            'physical_state': (r"F[\s]*?o[\s]*?r[\s]*?m[\s]*?\W(?P<data>.{30})", (re.S|re.I))
        },
        'sigma_aldrich': {
            'manufacturer': (r"(?P<data>\bsigma[\-\s]*?aldrich\b)", re.I),
            'product_name': (r"product\s*?name[\s:]*(?P<data>.*?)product", (re.S|re.I)),
            'flash_point': (r"flash\s*?point([\sC\d°:\(.]*?(?P<data>[0-9.]*)\s*?°?\s*?F)?", (re.S|re.I)),
            'specific_gravity': (r"relative\s*?density\D*(?P<data>[\d.]*)", (re.S|re.I)),
            'cas_number': (r"CAS(?P<data>.{30})", (re.S|re.I)),
            'nfpa_fire': (r"nfpa.*fire.*?(?P<data>\d)", (re.S|re.I)),
            'nfpa_health': (r"nfpa.*health.*?(?P<data>\d)", (re.S|re.I)),
            'nfpa_reactivity': (r"nfpa.*reactivity.*?(?P<data>\d)", (re.S|re.I)),
            'sara_311': (r"sara\s*?311\/312((?P<fire>fire hazard\s*)|(?P<acute>acute health hazard\s*)|(?P<chronic>chronic health hazard\s*)|(?P<reactive>reactive hazard\s*)|(?P<sudden>sudden release of pressure\s*)|\s|hazards)*", (re.S|re.I)),
            'revision_date': (r"revision\s*?date\D*(?P<data>[\d\-\/]{6,15})", (re.S|re.I)),
            'physical_state': (r"appearance.{0,10}form\W*(?P<data>\w*)", (re.S|re.I))
        },
        'symrise': {
            'manufacturer': (r"(?P<data>\bsymrise\b)", re.I),
            'product_name': (r"product\s*?name[\s:]*(?P<data>.*?)material", (re.S|re.I)),
            'flash_point': (r"flash\s*?point([\sC\d°:\(.]*?(?P<data>[0-9.]*)\s*?°?\s*?(F|C))?", (re.S|re.I)),
            'specific_gravity': (r"relative\s*?density[:\s]*(?P<data>[\d.]*)", (re.S|re.I)),
            'cas_number': (r"CAS(?P<data>.{30})", (re.S|re.I)),
            'nfpa_fire': (r"NFPA.*?[F|f]ire.*?(?P<data>[0-4])", (re.S|re.I)),
            'nfpa_health': (r"NFPA.*?[H|h]ealth.*?(?P<data>[0-4])", (re.S|re.I)),
            'nfpa_reactivity': (r"NFPA.*?(([R|r]eactivity)|([I|i]nstability)).*?(?P<data>[0-4])", (re.S|re.I)),
            'sara_311': (r"SARA 311(?P<data>.{80})", (re.S|re.I)),
            'revision_date': (r"revision\s*?date\D*(?P<data>[\d.]*)", (re.S|re.I)),
            'physical_state': (r"F[\s]*?o[\s]*?r[\s]*?m[\s]*?\W(?P<data>.{30})", (re.S|re.I))
        },
        'takasago': {
            'manufacturer': (r"(?P<data>takasago)", re.I),
            'product_name': (r"\s[P|p]roduct\s(?P<data>.{80})", (re.S|re.I)),
            'flash_point': (r"[F|f]lash\s*?[P|p]oint(?P<data>.{30})", (re.S|re.I)),
            'specific_gravity': (r"([R|r]elative [D|d]ensity|[S|s]pecific [G|g]ravity)(?P<data>.{30})", (re.S|re.I)),
            'cas_number': (r"CAS(?P<data>.{30})", (re.S|re.I)),
            'nfpa_fire': (r"NFPA.*?[F|f]ire.*?(?P<data>[0-4])", (re.S|re.I)),
            'nfpa_health': (r"NFPA.*?[H|h]ealth.*?(?P<data>[0-4])", (re.S|re.I)),
            'nfpa_reactivity': (r"NFPA.*?(([R|r]eactivity)|([I|i]nstability)).*?(?P<data>[0-4])", (re.S|re.I)),
            'sara_311': (r"SARA 311(?P<data>.{80})", (re.S|re.I)),
            'revision_date': (r"[R|r]evision [D|d]ate(?P<data>.{20})", (re.S|re.I)),
            'physical_state': (r"F[\s]*?o[\s]*?r[\s]*?m[\s]*?\W(?P<data>.{30})", (re.S|re.I))
        },
        'treatt': {
            'manufacturer': (r"(?P<data>\btreatt\b)", re.I),
            'product_name': (r"product\s*identifier.*?product\s*name\s*(?P<data>[^\d]+)", (re.S|re.I)),
            'flash_point': (r"flash\s*point.{1,50}?((?P<farenheit>\d[\d°\s,.]+°?\s*?f)|(?P<celcius>\d[\d°\s,“]+C(?![\d\s\(>,.°“\/]{1,50}?f)))", (re.S|re.I)),
            'specific_gravity': (r"(relative density|specific gravity)(?P<data>.{30})", (re.S|re.I)),
            'cas_number': (r"CAS(?P<data>.{30})", (re.S|re.I)),
            'nfpa_fire': (r"NFPA.*?[F|f]ire.*?(?P<data>[0-4])", (re.S|re.I)),
            'nfpa_health': (r"NFPA.*?[H|h]ealth.*?(?P<data>[0-4])", (re.S|re.I)),
            'nfpa_reactivity': (r"NFPA.*?(([R|r]eactivity)|([I|i]nstability)).*?(?P<data>[0-4])", (re.S|re.I)),
            'sara_311': (r"SARA 311(?P<data>.{80})", (re.S|re.I)),
            'revision_date': (r"revision\s*?date\s*(?P<data>[\d\-\w]*\d)", (re.S|re.I)),
            'physical_state': (r"physical\s*?state\s*(?P<data>[\w ]*)", (re.S|re.I))
        },
        'ungerer': {
            'manufacturer': (r"(?P<data>\bungerer\s*?and\s*?company\b)", re.I),
            'product_name': (r"product\s*?name\s*\w*\s?(?P<data>.*?)\d", (re.S|re.I)),
            'flash_point': (r"flash\s*?point[\s\dc€°\/]*?(?P<data>[\d.]*)\s*?[€°]*?\s*?f", (re.S|re.I)),
            'specific_gravity': (r"specific\s*?gravity\s*?(?P<data>[\d.]*)", (re.S|re.I)),
            'cas_number': (r"CAS(?P<data>.{30})", (re.S|re.I)),
            'nfpa_fire': (r"nfpa.*flammability.*?(?P<data>\d)", (re.S|re.I)),
            'nfpa_health': (r"nfpa.*health.*?(?P<data>\d)", (re.S|re.I)),
            'nfpa_reactivity': (r"nfpa.*instability.*?(?P<data>\d)", (re.S|re.I)),
            'sara_311': (r"sara\s*?311\/312(((?P<acute>acute health hazard)yes)|((?P<chronic>chronic health hazard)yes)|((?P<fire>fire hazard)yes)|((?P<sudden>sudden release of pressure hazard)yes)|((?P<reactive>reactive hazard)yes)|\s|hazard|categories|acute|health|yes|€|chronic|no|fire|sudden release of pressure|reactive)*", (re.S|re.I)),
            'revision_date': (r"revision\s*?date[:€\s]*(?P<data>[\d\-\/\w]*?)€", (re.S|re.I)),
            'physical_state': (r"physical\s*?state[\s\W\dc]*(?P<data>[\w]*)", (re.S|re.I))
        },
    }

    DEFAULT_SDS_FORMAT = {
        'manufacturer': (r"[C|c]ompany(?P<data>.{80})", (re.S|re.I)),
        'product_name': (r"\s[P|p]roduct\s(?P<data>.{80})", (re.S|re.I)),
        'flash_point': (r"[F|f]lash\s*?[P|p]oint(?P<data>.{30})", (re.S|re.I)),
        'specific_gravity': (r"([R|r]elative [D|d]ensity|[S|s]pecific [G|g]ravity)(?P<data>.{30})", (re.S|re.I)),
        'cas_number': (r"CAS(?P<data>.{30})", (re.S|re.I)),
        'nfpa_fire': (r"NFPA.*?[F|f]ire.*?(?P<data>[0-4])", (re.S|re.I)),
        'nfpa_health': (r"NFPA.*?[H|h]ealth.*?(?P<data>[0-4])", (re.S|re.I)),
        'nfpa_reactivity': (r"NFPA.*?(([R|r]eactivity)|([I|i]nstability)).*?(?P<data>[0-4])", (re.S|re.I)),
        'sara_311': (r"SARA 311(?P<data>.{80})", (re.S|re.I)),
        'revision_date': (r"[R|r]evision [D|d]ate(?P<data>.{20})", (re.S|re.I)),
        'physical_state': (r"F[\s]*?o[\s]*?r[\s]*?m[\s]*?\W(?P<data>.{30})", (re.S|re.I))
    }
