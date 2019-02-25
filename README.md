![alt text](https://github.com/astepe/sds_parser/blob/master/LogoSample_ByTailorBrands.jpg)

## SDSParser
SDSParser is a browser-based app for extracting chemical data from Safety Data Sheet documents. SDSParser will speed up your
data-entry process by eliminating the need to read through Safety Data Sheets to get the data you care about.

For a live demo, click here: [SDSParser](http://www.arisstepe.com/projects/submit_sds)

For testing purposes, here are some SDS files to download and use:
* [Fisher Scientific](https://www.fishersci.com/store/msds?partNumber=M2131&productDescription=MET+ISOBUTYL+KETONE+CR+ACS+1L&vendorId=VN00033897&countryCode=US&language=en)
* [Sigma Aldrich](https://www.sigmaaldrich.com/MSDS/MSDS/DisplayMSDSPage.do?country=US&language=en&productNumber=P5958&brand=SIGALD&PageToGoToURL=https%3A%2F%2Fwww.sigmaaldrich.com%2Fcatalog%2Fsearch%3Fterm%3Dpotassium%26interface%3DAll%26N%3D0%26mode%3Dmatch%2520partialmax%26lang%3Den%26region%3DUS%26focus%3Dproduct)

## Motivation
Built out of the need to quickly access chemical data from Safety Data Sheets for data-entry purposes. Each chemical manufacturer will stylize and structure their SDSs a little bit differently. SDSParser can easily be updated to read a new manufacturer format by adding a new set of regular expressions to match the format that that specific manufacturer uses.

## Tech/framework used
* [pdfminer](https://github.com/euske/pdfminer), a tool for extracting information from PDF documents
* [pytesseract](https://pypi.org/project/pytesseract/), a python wrapper for Google's Tesseract-OCR

## Features
Have some physical SDSs you need to scan and get data from? Have no fear, sds_parser will recognize your scanned file as an image and perform optical character recognition (ocr) to extract the text for you.

## How to install

`pip install SDSParser`

## How to use
Simply initialize `SDSParser` with an optional list of data fields you wish to extract (e.g. ['manufacturer', 'flash_point']) to the `request_keys` key-word argument. See `configs.SDSRegexes.REQUEST_KEYS` for the proper keys to use. If no keys are requested, all available data fields will be searched.

```
>>> from sdsparser import SDSParser
>>> request_keys = ['manufacturer', 'flash_point', 'specific_gravity', 'product_name', 'sara_311', 'nfpa_fire']
>>> parser = SDSParser(request_keys=request_keys)
```

Here is a list of the keys to use.
```
>>> from sdsparser.configs.SDSRegexes import REQUEST_KEYS
>>> REQUEST_KEYS
[
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
```

Call `parser.get_sds_data('path/to/ExampleSDS.pdf')` and pass in the path to your SDS document to get the sds data.

```
>>> sds_data = parser.get_sds_data('path/to/SafetyDataSheet.pdf')
```

`.get_sds_data` returns a dictionary object mapping request key names to their corresponding matches

```
>>> sds_data
{
 'manufacturer': 'Sigma-Aldrich',
 'product_name': 'Sodium dodecyl sulfate',
 'flash_point': '338 F',
 'specific_gravity': '3.2',
 'sara_311': 'Data not listed'
 'nfpa_fire': 'No data available'
}
```

If the heading for the requested data type is not found in the SDS, `.get_sds_data` will return the string 'Data not listed'.
If the heading is found, but no data is found under it, `.get_sds_data` will return the string 'No data available'.

## SDSParser-cli

In your terminal

```
path/to/sds/directory $ sdsparser parse --flash_point --specific_gravity
{'fisher_1.pdf': {'flash_point': 'No data available',
                  'specific_gravity': 'No data available'},
 'fisher_2.pdf': {'flash_point': 'No data available',
                  'specific_gravity': 'No data available'},
 'fisher_3.pdf': {'flash_point': 'No data available',
                  'specific_gravity': '1.84'},
 'fisher_5.pdf': {'flash_point': 'No data available',
                  'specific_gravity': 'No data available'}}
```
or
```
path/to/sds/directory $ sdsparser parse --csv
path/to/sds/directory $ cat sds_data.csv
Fisher,Data not listed,No data available,No data available,1,0,0,/312 Hazard CategoriesSee section 2 for more informationCWA (Clean Water Act)Not,26-Jan-2018,Powder,Data not listed
Fisher,"Salicylic acid, sodium salt",No data available,(etc...)
```
for more information
```
$ sdsparser --help
```
or
```
$ sdsparser parse --help
```

## License

MIT © [Aris Stepe](http://www.arisstepe.com/)
