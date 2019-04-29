from .helpers import get_pdf_text, get_pdf_image_text

from .regexes import get_manufacturer_name, get_static_regexes, \
                     search_sds_text

from .configs import Configs


class SDSParser:

    def __init__(self, request_keys=None, file_info=False):
        """
        The SDSParser object performs regular expression matching on safety
        data sheets based on specific formats created by common chemical
        manufacturers.

        :param request_keys: a list of strings that define the desired fields
                             from safety data sheet (see configs.REQUEST_KEYS
                             for a list of valid search keys)
        :param file_info: input True to include extra file information in the
                          output.
        """

        if isinstance(request_keys, list) and request_keys:
            self.request_keys = request_keys
        else:
            self.request_keys = Configs.REQUEST_KEYS

        self.ocr_override = True
        self.ocr_ran = False
        self.force_ocr = False

        self.file_info = file_info

    def get_sds_data(self, sds_file_path, extract_method=''):
        """
        The get_sds_data method determines the manufacturer of the given safety
        data sheet and retrieves the corresponding regular expression matches.

        :param sds_file_path: Path to a safety data sheet file in .pdf format
        :param extract_method: Define the text extraction method. Set to 'ocr'
                               to extract text using only Optical Character
                               Recognition. Set to 'text' to extract text using
                               only standard text extraction.

                               If no input is given, SDSParser will dynamically
                               select an extraction method based on various
                               criteria.
                               (see get_sds_text for full logic flow)

        get_sds_data will return a dictionary object mapping user-defined
        request keys to resultant text matches. i.e.:
        {
        'flash_point': 102F,
        'specific_gravity': 1.102
        }
        """

        self.reset_state()
        self.sds_file_path = sds_file_path
        self.set_extract_method(extract_method)

        self.sds_text = self.get_sds_text(sds_file_path)

        self.manufacturer_name = get_manufacturer_name(self.sds_text)
        regexes = get_static_regexes(self.manufacturer_name,
                                     request_keys=self.request_keys)

        self.sds_data = search_sds_text(self.sds_text,
                                        regexes[self.manufacturer_name])

        if self.data_not_listed() and not self.ocr_ran and self.ocr_override:
            self.sds_data = self.get_sds_data(sds_file_path,
                                              extract_method='ocr')

        if self.file_info:
            self.sds_data.update(self.get_file_info())

        return self.sds_data

    def data_not_listed(self):
        """
        Returns True if no matches were found in safety data sheet text. This
        frequently indicates corrupted or unreadable text and is used to
        determine if optical character recognition should be executed
        on the file instead of conventional text extraction methods.
        """

        for _, data in self.sds_data.items():
            if data.lower() != 'data not listed':
                return False
        return True

    def reset_state(self):
        """
        resets booleans that keep track of when and if ocr should be utilized
        """
        self.ocr_override = True
        self.ocr_ran = False
        self.force_ocr = False

    def set_extract_method(self, extract_method):
        """
        sets text-extraction method
        :param extract_method: 'ocr' to use optical character recognition and
                               'text' to use standard text extraction
        """
        if extract_method == 'ocr':
            self.force_ocr = True
        if extract_method == 'text':
            self.ocr_override = False

    def get_sds_text(self, sds_text_source):
        """
        Executes the text extraction function corresponding to the
        specified extract method and current ocr state. If a matching text file
        is found in the user-defined directory, text will be retrieved from
        the corresponding .txt file if it is found.

        If no text is able to be extracted using standard text extraction
        methods, ocr with be executed unless the user has specified
        to only use standard methods or ocr has already been
        executed on the particular file.

        :param file_path: A path to a safety data sheet file in .pdf format
        """

        if self.force_ocr:
            extract_text = self.extract_with_ocr
        else:
            extract_text = self.extract_with_fallback

        return extract_text(sds_text_source)

    def extract_with_fallback(self, file_path):
        """
        Try to get the text directly from pdf, if no text is found, run ocr
        """
        sds_text = get_pdf_text(file_path)
        if sds_text == '' and self.ocr_override and not self.ocr_ran:
            sds_text = self.extract_with_ocr(file_path)
        return sds_text

    def extract_with_ocr(self, file_path):
        sds_text = get_pdf_image_text(file_path)
        self.ocr_ran = True
        return sds_text

    def get_file_info(self):
        """
        Retrieve extra information on safety data sheet file. Used for
        development and debugging.
        """
        file_info = {
                     'format': self.manufacturer_name,
                     'file_name': self.sds_file_path.split('/')[-1],
                     'ocr_ran': self.ocr_ran,
                     }

        return file_info
