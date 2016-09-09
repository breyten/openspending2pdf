#!/usr/bin/env python

import os
import sys
import re
from pprint import pprint

import requests
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        # Logo
        #self.image('logo_pb.png', 10, 8, 33)
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(30, 10, 'Title', 1, 0, 'C')
        # Line break
        self.ln(20)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

class OpenspendingAPI(object):
    def __init__(self, *args, **kwargs):
        self.base_url = 'http://openspending.nl/api/v1/'

    def main(self, year, period, gov_code, direction):
        return requests.get(
            '%saggregations/main/?year=%s&period=%s&gov_code=%s&direction=%s' % (
                self.base_url, year, period, gov_code, direction,)).json()

    def labels(self, document_id, direction):
        return requests.get(
            '%slabels/?document_id=%s&direction=%s&limit=500' % (
                self.base_url, document_id, direction,)).json()



def main():
    os = OpenspendingAPI()
    labels = {l['code']: l for l in os.labels(7214, 'out')['objects']}
    #pprint(labels.keys())
    main_functions = {m[u'term']: m[u'total'] for m in os.main(2015, 0, '0344', 'out')['facets']['terms']['terms']}

    # Instantiation of inherited class
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Times', '', 12)
    #pprint(main_functions)
    for main_function, total in main_functions.iteritems():
        pdf.cell(
            0, 10,
            "%s. %s %s" % (
                main_function, labels[main_function][u'label'], total,), 0, 1)

    pdf.output('utrecht.pdf', 'F')

if __name__ == '__main__':
    main()
