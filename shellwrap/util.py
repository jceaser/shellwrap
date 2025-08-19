#!/usr/bin/env python3

""" General functions of no specific category """

#mark - Imports

import json

#mark - functions

def str_to_json(foo):
    return lambda *flags : json.loads(foo(*flags))
