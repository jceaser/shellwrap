# pylint datetools.py
# count lines of code with:
# sed -n '/^#cloc-start$/,/^#cloc-end$/p' template.py | cloc - --stdin-name=template.py

#cloc-start

# template modified 2021-09-02

""" Functions for getting Date and Time values """

#mark - Imports

import datetime
import time

# ######################################
#mark date functions

def now_internal():
    """ In testing, this one function can be Mocked to stop time """
    return datetime.datetime.now()

def now():
    """ Return a string with the current date and time formated in ISO"""
    return now_internal().strftime("%Y-%m-%dT%H:%M:%S")

def today():
    """ Return a string with the current date formated in ISO"""
    return now_internal().strftime("%Y-%m-%d")

def unix():
    """ unix time stamp """
    return int(time.time())

def unix_difference(start):
    """ different from a unix start time stamp and now """
    return int(time.time()) - start
