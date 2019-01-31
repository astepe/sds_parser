from distutils.core import setup
import os

setup(
    name='SDSParser',
    version='0.1.0',
    author='A. Stepe',
    author_email='arisstepe@gmail.com',
    packages=['sdsparser'],
    scripts=['bin/update_sds.py'],
    url='https://github.com/astepe/sds_parser',
    license='LICENSE.txt',
    description='Extract chemical data from Safety Data Sheet documents',
    long_description=open('README.md').read(),
    install_requires=[
        "chardet==3.0.4",
        "pdf2image==1.4.0",
        "pdfminer.six==20181108",
        "Pillow==5.4.1",
        "progressbar==2.5",
        "pycryptodome==3.7.3",
        "pytesseract==0.2.6",
        "six==1.12.0",
        "sortedcontainers==2.1.0",
    ],
)
