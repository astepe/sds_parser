import re
import os
import csv
from PyPDF2 import PdfFileReader
from collections import namedtuple


#def get_text_from_image(image):

#    pages = pdf2image.convert_from_path(os.path.join(file_folder, sds_file), 500)
#
#    image_folder_name = sds_file.split('.')[0]
#    image_folder_full_path = os.path.join(os.getcwd(), 'sds_images', image_folder_name)
#    for idx, page in enumerate(pages):
#        if not os.path.exists(image_folder_full_path):
#            os.mkdir(image_folder_name)
#        image_file_full_path = image_folder_full_path + f'/page_{idx+1}.jpg'
#        page.save(image_file_full_path, 'JPEG')
#
#    image_folder = os.listdir(image_folder_full_path)
#
#    sds_image_text = ''
#
#    for image in image_folder:
#        image_path = os.path.join(image_folder_full_path, image)
#
#        sds_image_text += pytesseract.image_to_string(Image.open(image_path))


class SDSRegexes:

    # SDS_FORMAT_REGEXES is a dict mapping manufacturer names ('Takasago', 'Robertet', etc.)
    # to a dict of regexes specific to the manufacturer SDS format where the keys are data_request_keys
    # and the values are regexes for those specific data searches
    SDS_FORMAT_REGEXES = {

        'Citrus and Allied': {
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
        'Excellentia': {
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
        'Firmenich': {
            'manufacturer': (r"(?P<data>\bfirmenich\b)", re.I),
            'product_name': (r"(chemical\s*?name|product)[\s:\d\w\-]*?(?P<data>[^\-\d:]*?)(revised|synonyms)", (re.S|re.I)),
            'flash_point': (r"flash\s*?point.*?((?P<fahrenheit>\d[\d.,\s]*)°?\s*?(\bF\b|Fahrenheit)|(?P<celsius>\d[\d.,\s]*)°?C(?!.{1,50}?(\bF\b|Fahrenheit)))", (re.S|re.I)),
            'specific_gravity': (r"([R|r]elative [D|d]ensity|[S|s]pecific [G|g]ravity)(?P<data>.{30})", (re.S|re.I)),
            'cas_number': (r"CAS(?P<data>.{30})", (re.S|re.I)),
            'nfpa_fire': (r"NFPA.*?[F|f]ire.*?(?P<data>[0-4])", (re.S|re.I)),
            'nfpa_health': (r"NFPA.*?[H|h]ealth.*?(?P<data>[0-4])", (re.S|re.I)),
            'nfpa_reactivity': (r"NFPA.*?(([R|r]eactivity)|([I|i]nstability)).*?(?P<data>[0-4])", (re.S|re.I)),
            'sara_311': (r"SARA 311(?P<data>.{80})", (re.S|re.I)),
            'revision_date': (r"[R|r]evision [D|d]ate(?P<data>.{20})", (re.S|re.I)),
            'physical_state': (r"F[\s]*?o[\s]*?r[\s]*?m[\s]*?\W(?P<data>.{30})", (re.S|re.I))
        },
        'Frutarom': {
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
        'Givaudan': {
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
        'IFF': {
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
        'Kerry': {
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
        'PepsiCo Inc': {
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
        'Robertet': {
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
        'Sigma Aldrich': {
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
        'Symrise': {
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
        'Takasago': {
            'manufacturer': (r"(?P<data>\btakasago\b)", re.I),
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
        'Treatt': {
            'manufacturer': (r"(?P<data>\btreatt\b)", re.I),
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
        'Ungerer and Company': {
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

    # SDS_DATA_TITLES is a dict mapping data request keys ('flash_point', 'specific_gravity', etc.)
    # to string titles ('Flash Point (°F)', 'Specific Gravity', etc.)
    SDS_DATA_TITLES = {
        'manufacturer': 'Manufacturer',
        'product_name': 'Product Name',
        'flash_point': 'Flash Point (°F)',
        'specific_gravity': 'Specific Gravity',
        'nfpa_fire': 'NFPA Fire',
        'nfpa_health': 'NFPA Health',
        'nfpa_reactivity': 'NFPA Reactivity',
        'sara_311': 'SARA 311/312',
        'revision_date': 'Revision Date',
        'physical_state': 'Physical State',
        'cas_number': 'CAS # (if pure)'
    }

    REQUEST_KEYS = [key for key, _ in SDS_DATA_TITLES.items()]


class SDSParser(SDSRegexes):

    def __init__(self, request_keys=None):

        if request_keys is not None:
            self.request_keys = request_keys
        else:
            self.request_keys = self.REQUEST_KEYS

    def get_sds_data(self, sds_file):

        self.sds_text = SDSParser.extract_text(sds_file)

        if self.sds_text == '':
            print(sds_file, 'no text found')

        regexes = self.get_format_regexes()

        sds_data = {}

        for request_key in self.request_keys:

            if request_key in regexes:

                title = self.SDS_DATA_TITLES[request_key]
                regex = regexes[request_key]
                match = self.find_match(regex)

                if request_key == 'manufacturer':
                    sds_data[title] = match.lower().title()
                else:
                    sds_data[title] = match

        return sds_data

    def find_match(self, regex):

        match = regex.search(self.sds_text)

        if match is not None:

            match_string = ''
            group_matches = 0
            for name, group in match.groupdict().items():
                if group is not None:
                    group = group.replace('\n', '').strip()
                    if group_matches > 0:
                        match_string += ', ' + group
                    else:
                        match_string += group
                    group_matches += 1

            if match_string:
                return match_string
            else:
                return 'No data available'

        else:

            return 'Data not listed'

    def get_format_regexes(self):

        # set initial format to default
        format_regexes = self.DEFAULT_SDS_FORMAT

        for manufacturer, regexes in self.SDS_FORMAT_REGEXES.items():

            #print(manufacturer)
            #print(regexes['manufacturer'])
            regex = re.compile(*regexes['manufacturer'])

            match = regex.search(self.sds_text)

            if match:# and match.group('data'):
                format_regexes = dict(regexes)
                print(f'using {manufacturer} format')
                return SDSParser.compile_regexes(format_regexes)

        #print(format_regexes['manufacturer'])
        print('using default sds format')
        return SDSParser.compile_regexes(format_regexes)

    @staticmethod
    def compile_regexes(regexes):

        compiled_regexes = {}

        for name, regex in regexes.items():

            compiled_regexes[name] = re.compile(*regex)

        return compiled_regexes

    @staticmethod
    def extract_text(file_path):

        text = ''

        with open(file_path, "rb") as _:
            pdf = PdfFileReader(_, 'rb')
            try:
                for page_num in range(pdf.getNumPages()):
                    # TODO: unknown error from certain files
                    try:
                        text += pdf.getPage(page_num).extractText()
                    except:
                        pass
            except:
                print('encryption algorithm is not supported')

        # print(file_path)
        # file_name = file_path.split('/')[-1].split('.')[0]
        # with open(os.path.join(os.getcwd(), f'{file_name}.txt'), 'w') as text_file:
        #     text_file.write(text)
        return text


if __name__ == '__main__':
    sds_folder = os.getcwd() + '/sds_pdf_files'
    sds_parser = SDSParser()

    with open('chemical_data.csv', 'w') as _:
        writer = csv.writer(_)
        writer.writerow([SDSParser.SDS_DATA_TITLES[key] for key in sds_parser.request_keys])

        for file in os.listdir(sds_folder):
            chemical_data = sds_parser.get_sds_data(os.path.join(sds_folder, file))
            writer.writerow([data for category, data in chemical_data.items()])

# flash\s*point.{1,50}?((?P<farenheit>\d[\d°\s,]+F)|(?P<celcius>\d[\d°\s,]+C(?!.*?f)))
