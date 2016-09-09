#!/usr/bin/env python

import os
import sys
import re
from pprint import pprint

import requests

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
    #pprint(main_functions)
    for main_function, total in main_functions.iteritems():
        print "%s. %80s\t\t%-15s" % (main_function, labels[main_function][u'label'], total)
if __name__ == '__main__':
    main()
