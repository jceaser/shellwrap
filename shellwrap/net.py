#!/usr/bin/env python3

""" Functions for making HTTP requests """

#mark - Imports

import json
import urllib.request
#import requests

def str_to_json(foo):
    return lambda *flags : json.loads(foo(*flags))

def read(url):
    ret = ""
    try:
        resp = urllib.request.urlopen(url)
        ret = resp.read()
    except urllib.error.HTTPError as e:
        ret = 'HTTPError: {} - {}'.format(e.code, e.reason)
        ret = {'status': e.code,
            'headers': e.headers.items(),
            'text': e.read().decode()}
    return ret
