#!/usr/bin/env python3

# pylint template.py
# count lines of code with:
# sed -n '/^#cloc-start$/,/^#cloc-end$/p' template.py | cloc - --stdin-name=template.py

#cloc-start

# template modified 2021-09-02

""" template script for future scripts """

#mark - Imports

#from enum import Enum   #Creating Enums
#import argparse         #command line parsing
#import code             #interactive shell
import os               #file handling
#import re               #filter in man()
#import readline         #interactive shell
#import subprocess       #calling unix commands
#import sys              #exiting

# ######################################
#mark File Tools

def read_file(path:str=None):
    """
    Read and return the contents of a file
    Parameters:
        path (string): full path to file to read
    Returns:
        None if file was not found, contents otherwise
    """
    text = None
    path=os.path.realpath(__file__[:-2]+"txt") if path is None else os.path.expanduser(path)
    if os.path.isfile(path):
        with open(path, "r") as file:
            text = file.read().strip()
            file.close()
    return text

def write_file(text:str, path:str=None):
    """
    Write (creating if need be) file and set it's content
    Parameters:
        path (string): path to file to write
        text (string): content for file
    """
    path=os.path.realpath(__file__[:-2]+"txt") if path is None else os.path.expanduser(path)
    with open(path, "w+") as cache:
        cache.write(text)
        cache.close()
