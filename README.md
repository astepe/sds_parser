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

## How to use?
Simply initialize `SDSParser` with an optional list of data fields you wish to extract (e.g. ['manufacturer', 'flash_point']) to `request_keys`. See `configs.SDSRegexes.SDS_DATA_TITLES` for the proper keys to use. If no keys are requested, all available data fields will be searched.
```
sds_parser = SDSParser(**request_keys=<[keys]>)
```
then call `.get_sds_data()` to retrieve the matches by passing in your SDS document in `.pdf` format. If you wish to turn off automatic ocr functionality, do that here with `ocr_override=False`.
```
chemical_data = sds_parser.get_sds_data(file_path, ocr_override=False)
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
