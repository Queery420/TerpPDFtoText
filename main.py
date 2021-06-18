# Cannabis Terpene Data PDF to Text Converter
# Written by Ivy Slick (@Queery420) on 6/11/21
# This program uses tabula.py, a PDF text-and-table extraction tool.
# (https://github.com/chezou/tabula-py)
#
# This program extracts text from Cannabanoid and Terpene Content PDFs
# from growers and manufactures operating within the Maryland Medical
# Cannabis Industry and formats it for use in labeling or posting to
# a website.
#
# Code logic
# >Scan program folder for PDFs
# >Extract Text & Tables from PDFs
# >Search extracted data for:
# >>Strain Name
# >>RFID
# >>Cannabanoid Content
# >>Terpene Content
# >Format and Print Found information to text files

import os
import tabula
