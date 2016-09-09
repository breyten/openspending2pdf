#!/usr/bin/env python

import os
import sys
import re

import requests
import pdfkit

def main():
    url = 'http://www.openspending.nl/utrecht-gemeente/realisatie/2016/lasten/hoofdfuncties/'
    pdfkit.from_url(url, 'utrecht.pdf')

if __name__ == '__main__':
    main()
