#!/usr/bin/env python

import os
import sys
import re

import requests
import pdfkit

def main():
    options = {
        #'quiet': '',
        'user-style-sheet': 'os2pdf.css',
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None
    }
    url = 'http://www.openspending.nl/utrecht-gemeente/realisatie/2016/lasten/hoofdfuncties/'
    pdfkit.from_url(url, 'utrecht.pdf', options=options)

if __name__ == '__main__':
    main()
