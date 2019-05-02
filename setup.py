from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='SDSParser',
    version='0.2.2',
    author='A. Stepe',
    author_email='aris@stepe.email',
    packages=find_packages(exclude=['tests', 'dev_tools']),
    package_data={'sdsparser': ['static/*']},
    url='https://github.com/astepe/sds_parser',
    license='LICENSE.txt',
    description='Extract chemical data from Safety Data Sheet documents',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        "chardet>=3.0.4,<3.1",
        "pdf2image>=1.4.0,<1.5",
        "pdfminer.six==20181108",
        "Pillow>=5.4.1,<5.5.0",
        "pycryptodome>=3.7.3,<3.8.0",
        "pytesseract>=0.2.6,<0.3.0",
        "six>=1.12.0,<2.0.0",
        "sortedcontainers>=2.1.0,<2.2.0",
        "tabulate>=0.8.3,<0.9.0",
        "tqdm>=4.31.1,<4.32.0"
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'sdsparser = sdsparser.__main__:main'
        ]
    },

)
