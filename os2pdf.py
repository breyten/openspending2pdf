#!/usr/bin/env python
# -*- coding: utf-8 -*-

import locale
import os
import sys
import re
from pprint import pprint

import requests
from fpdf import FPDF

class PDF(FPDF):
    def __init__(self, *args, **kwargs):
        super(PDF, self).__init__()
        self.doc = kwargs['doc']
        self.periods = {
            0: 'begroting',
            5: 'realisatie'
        }

    def header(self):
        # Logo
        #self.image('logo_pb.png', 10, 8, 33)
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Move to the right
        # self.cell(80)
        # Title
        title = 'Openspending - %s - %s %s' % (
            self.doc['government']['name'],  self.periods[self.doc['period']], self.doc['year'],)
        self.cell(30, 10, title, 0, 0)
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

    def document(self, id):
        return requests.get('%sdocuments/%s/' % (self.base_url, id,)).json()

    def main(self, year, period, gov_code, direction):
        return requests.get(
            '%saggregations/main/?year=%s&period=%s&gov_code=%s&direction=%s' % (
                self.base_url, year, period, gov_code, direction,)).json()

    def labels(self, document_id, direction):
        return requests.get(
            '%slabels/?document_id=%s&direction=%s&limit=500' % (
                self.base_url, document_id, direction,)).json()



def main():
    locale.setlocale( locale.LC_ALL, '' )
    os = OpenspendingAPI()
    doc = os.document(7214)
    labels = {l['code']: l for l in os.labels(doc['id'], 'out')['objects']}
    #pprint(labels.keys())
    main_functions_raw = os.main(doc['year'], doc['period'], doc['government']['code'][2:], 'out')
    main_functions = {m[u'term']: m[u'total'] for m in main_functions_raw['facets']['terms']['terms']}
    total = main_functions_raw['facets']['total']['total']
    # Instantiation of inherited class
    pdf = PDF(doc=doc)
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Times', '', 12)
    pdf.set_font('Times', 'B', 12)
    pdf.cell(
        0, 10,
        'Totaal', 0, 1)
    pdf.set_font('Times', '', 12)
    pdf.cell(0, 10, "%s" % (locale.currency(total, '€', '.'),), 0, 1)
    pdf.cell(190, 2, '', 0, 1, '', True)
    for main_function, amount in sorted(main_functions.iteritems()):
        pdf.set_font('Times', 'B', 12)
        pdf.cell(
            0, 10,
            "%s. %s" % (
                main_function, labels[main_function][u'label'],), 0, 1)
        pdf.set_font('Times', '', 12)
        pdf.cell(0, 10, "%s" % (locale.currency(amount, '€', '.'),), 0, 1)
        pdf.cell((amount * 190 / total), 2, '', 0, 1, '', True)

    pdf.output('utrecht.pdf', 'F')

if __name__ == '__main__':
    main()
