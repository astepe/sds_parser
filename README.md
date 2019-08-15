![alt text](https://github.com/astepe/sds_parser/blob/master/LogoSample_ByTailorBrands.jpg)

## SDSParser
SDSParser is a Python library and command line tool for extracting chemical data from Safety Data Sheet documents. SDSParser will speed up your
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

## Dependencies
SDSParser requires that poppler and tesseract tools are install on your local system and included on your PATH

## How to use
Simply initialize `SDSParser` with an optional list of data fields you wish to extract (e.g. ['manufacturer', 'flash_point']) to the `request_keys` key-word argument. See `sdsparser.request_keys` for the proper keys to use. If no keys are requested, all available data fields will be searched.

```
>>> from sdsparser import SDSParser
>>> request_keys = \
['manufacturer', 'flash_point', 'specific_gravity', 'product_name', 'sara_311', 'nfpa_fire']
>>> parser = SDSParser(request_keys=request_keys)
```

Here is a list of the keys to use.
```
>>> import sdsparser
>>> sdsparser.request_keys
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

To see a set of all of the currently supported chemical manufacturers:
```
>>> import sdsparser
>>> sdsparser.manufacturers
{'the_clorox_company', 'firmenich', 'frutarom', 'symrise', 'exxon_mobil', 'fisher', 'indofine',
'ungerer','formosa_plastics', 'innophos', 'basf', 'citrus_and_allied', 'robertet',
'acros_organics', 'kerry', 'iff', 'treatt', 'excellentia', 'sigma_aldrich', 'takasago',
'givaudan', 'pepsico_inc', 'sc_johnson', 'pfizer', 'reckitt_benckiser', 'alfa_aesar'}
```

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

## dev_tools - regex_developer
Easily edit and update existing regular expressions with the help of a local MongoDB server and a GUI for making your changes.

For mongodb installation instructions go [here](https://docs.mongodb.com/v3.2/administration/install-community/)

1. Start by entering into the dev_tools folder, activate your virtalenv and run the command `python3.7 regex_developer.py`. Login as root to allow `mongod` to start the local server.

2. Use the top two drop-down menus to select both the manufacturer and regular expression you would like to test.
![alt text](https://github.com/astepe/sds_parser/blob/master/regex_developer_select_crop.jpg)

3. Click 'Get Regex' to populate the input field with the regular expression
![alt text](https://github.com/astepe/sds_parser/blob/master/regex_developer_get_crop.jpg)

4. Click 'Execute' to perform the match with the currently entered regular expression
![alt text](https://github.com/astepe/sds_parser/blob/master/regex_developer_execute_crop.jpg)

5. Make changes to your regular expression according to the tabulated output in the terminal, click 'Execute' again.
![alt text](https://github.com/astepe/sds_parser/blob/master/regex_developer_make_change_crop.jpg)

6. Rinse and repeat.

When you are ready to save your new and improved regular expression, click 'Save Regex'. This will store the text currently in the text input field to the MongoDB database. When you are ready to add your changes to `sdsparser`, export your regular expressions to /sdsparser/static/regexes.json. This can be accomplished using this command:

* `mongoexport -d sdsparser -c sdsRegexes --jsonArray -o regexes1.json --pretty`

# FAQ

## **How do I add new manufacturer support?**

1. Run the function `dev_tools.sds_file_manager.add_new_manufacturer`.
    * This will create two separate directories to store SDSs. 
    `sds_pdf_files/` stores SDS pdfs for that particular manufacturer. 
    `sds_text_files/` stores the resulting .txt files after text from the pdf files has been extracted. 
    Once the text files have been generated by `sds_file_manager`, `regex_developer` can use the text found there to perform regex matching instead of re-extracting the text from the pdf file directly.

2. Move your SDS files to the new directory found in `sds_pdf_files`
    * As long as you know the manufacturer for each SDS and that they are all of the same manufacturer, there is no need to rename the files. When `regex_developer` is started, `sds_file_manager` will update pdf file names, extract the text from the pdf files and save them to the corresponding directory within `sds_text_files/`.

3. Start `regex_developer` and follow the instructions from the in the console.
    * `regex_developer` will look for any new directories by comparing directory names with manufacturer names found in mongoDB. If a new directory is found, the user will be asked if they want to add the new manufacturer to mongoDB with the same name as the directory that was found. By choosing yes, the new manufacturer will be added to mongoDB using the default set of regular expressions.

4. The new manufacturer will now be available in the regex developer GUI.

## **Why are some txt files in sds_text_files suffixed with "_ocr.txt" and some with "_pdf.txt"?**
A user named Tom wants to add a new manufacturer named "acme" to sdsparser. After he generates the new directories using `dev_tools.sds_file_manager.add_new_manufacturer`, he moves 3 "acme" SDSs to the new directory `sds_pdf_files/acme/`. When he starts up `regex_developer`, he sees that his 3 SDSs were renamed to `amce_1.pdf`, `amce_2.pdf`, `amce_3.pdf`. He also sees 3 .txt files in `sds_text_files/acme/` named `acme_1_pdf.txt`, `acme_2_ocr.txt` and `acme_3_pdf.txt`. `acme_1_pdf.txt` contains text extracted from `amce_1.pdf` using standard text extraction methods while `acme_2_ocr.txt` contains text extracted from `amce_2.pdf` using optical character recognition. The content found in `amce_2.pdf` may be corrupted or each page may be an image which doesn't contain any real text.

## **How do I add new request keys?**
TODO

## License

MIT © [Aris Stepe](http://www.arisstepe.com/)
