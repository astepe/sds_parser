![alt text](https://github.com/astepe/sds_parser/blob/master/LogoSample_ByTailorBrands.jpg)

## sds_parser
sds_parser is a browser-based app for extracting chemical data from Safety Data Sheet documents. sds_parser will speed up your
data-entry process by eliminating the need to read through Safety Data Sheets to get the data you care about.

## Motivation
Built out of the need to quickly access chemical data from Safety Data Sheets for data-entry purposes. Each chemical manufacturer will stylize and structure their SDSs a little bit differently. sds_parser can easily be updated to read a new manufacturer format by adding a new set of regular expressions to match the format that that specific manufacturer uses. 

## Screenshots
Include logo/demo screenshot etc.

## Tech/framework used
* [pdfminer](https://github.com/euske/pdfminer), a tool for extracting information from PDF documents
* [pytesseract](https://pypi.org/project/pytesseract/), a python wrapper for Google's Tesseract-OCR

## Features
Have some physical SDSs you need to scan and get data from? Have no fear, sds_parser will recognize your scanned file as an image and perform optical character recognition to extract the text for you. 

## Code Example

```
 def get_sds_data(self, sds_file_path, **kwargs):
        """
        retrieve requested sds data
        """
        # set ocr configuration
        self.ocr = False
        self.ocr_override = True
        if 'ocr' in kwargs:
            self.ocr = kwargs['ocr']
            self.ocr_override = False
        
        # extract text from SDS
        self.sds_text = self.get_sds_text(sds_file_path)
        
        # locate manufacturer to choose regular expression set
        manufacturer = self.get_manufacturer(self.sds_text)
        
        # define dictionary of regular expressions based on found manufacturer
        if manufacturer is not None:
            regexes = SDSParser.compile_regexes(SDSRegexes.SDS_FORMAT_REGEXES[manufacturer])
        else:
            manufacturer = 'unknown'
            regexes = SDSParser.compile_regexes(SDSRegexes.DEFAULT_SDS_FORMAT)
        
        # perform string matching with regular expressions
        sds_data = self.search_sds_text(self.sds_text, regexes)
        
        # check for empty/junk text and route to ocr if so
        data_not_listed = SDSParser.check_empty_matches(sds_data)
        sds_data['format'] = manufacturer
        sds_data['filename'] = sds_file_path.split('/')[-1]
        if data_not_listed and not self.ocr and self.ocr_override:
            print(f'No matches found in {sds_file_path}. Performing ocr...')
            sds_data = self.get_sds_data(sds_file_path, ocr=True)
         
        return sds_data
```
Show what the library does as concisely as possible, developers should be able to figure out **how** your project solves their problem by looking at the code example. Make sure the API you are showing off is obvious, and that your code is short and concise.

## Installation
Provide step by step series of examples and explanations about how to get a development env running.

## How to use?
Simply initialize `SDSParser` with an optional list of data fields you wish to extract (e.g. ['manufacturer', 'flash_point']) to `request_keys`. See `configs.SDSRegexes.SDS_DATA_TITLES` for the proper keys to use. If no keys are requested, all available data fields will be searched.
```
sds_parser = SDSParser(**request_keys=<[keys]>)
```
then call `.get_sds_data()` to retrieve the matches by passing in your SDS document in `.pdf` format. If you wish to turn off automatic ocr functionality, do that here with `ocr=False`.
```
chemical_data = sds_parser.get_sds_data(file_path, ocr=False)
```
`chemical_data` will be a dictionary object mapping request key names to their corresponding matches. If the specific field is not found in the SDS, `.get_sds_data()` will return the string 'Data not listed'. If the field is found, but no data is found under it, `.get_sds_data()` will return the string 'No data available'.

## Contribute

Let people know how they can contribute into your project. A [contributing guideline](https://github.com/zulip/zulip-electron/blob/master/CONTRIBUTING.md) will be a big plus.

## Credits
Give proper credits. This could be a link to any repo which inspired you to build this project, any blogposts or links to people who contrbuted in this project. 

#### Anything else that seems useful

## License
A short snippet describing the license (MIT, Apache etc)

MIT © [Yourname]()
