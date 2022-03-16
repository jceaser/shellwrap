# pylint datetools.py
# count lines of code with:
# sed -n '/^#cloc-start$/,/^#cloc-end$/p' template.py | cloc - --stdin-name=template.py

#cloc-start

# template modified 2021-09-02

""" template script for future scripts """

#mark - Imports

import datetime

# ######################################
#mark date functions

def now():
    """ Return a string with the current date and time formated in ISO"""
    return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

def today():
    """ Return a string with the current date formated in ISO"""
    return datetime.datetime.now().strftime("%Y-%m-%d")
