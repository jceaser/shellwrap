#!/usr/bin/env python3

# pylint template.py
# count lines of code with:
# sed -n '/^#cloc-start$/,/^#cloc-end$/p' template.py | cloc - --stdin-name=template.py

#cloc-start

# template modified 2021-09-02

""" Terminal codes for drawing colors and styles on text """

#mark - Imports

from enum import Enum   #Creating Enums

# ##############################################################################
#mark - Utility functions - Leave these alone

class VMode(Enum):
    """ Verbose Mode Enums, higher values print less"""
    FATAL = -8 # always print
    ERROR = 0
    NORMAL = 1
    WARN = 2
    INFO = 4
    DEBUG = 8

class TerminalCode(dict):
    """
    A custom dictionary for storing terminal color codes that allows for value
    reuse. To add a duplicate value, prefix the key name with an arrow as the
    value for the new entry
    """
    def __init__(self, data):
        """
        Take in a dictionary, but look at values and decided if they should be
        reused
        """
        super().__init__()
        for key, value in data.items():
            self[key] = self[value[2:]] if value.startswith('->') else value

    def __getattr__ (self, attr):
        """ Allow items to be access with dot notation. """
        color_code = self.get(attr, '\033[0m')
        if color_code.startswith('\033'):
            return color_code
        return f'\033[0;{color_code}m'

    def full(self, fg, bg):
        fgc = self.get(fg, "0")
        bgc = self.get(bg, "0")
        return f'\033[{fgc};{bgc}m'
    def raw(self, code):
        return self.get(code, '0')

#https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences

"""Colors for the following schemas:
* RGB - Red, Green, Blue
* RYG - Red, Yellow, Green
* CMYK - Cyan, Magenta, Yellow, Black
"""
tcode = TerminalCode({'none': '\033[0m',
    'bold': '\033[1m',
    'faint': '\033[2m',
    'italix': '\033[3m',    #not well supported
    'underline': '\033[4m',
    'slow': '\033[5m',
    'fast': '\033[6m',      #not well supported
    'inverse': '\033[7m',
    'hide': '\033[8m',

    'off_bold': '\033[21m',
    'off_faint': '\033[22m',
    'off_italix': '\033[23m',    #not well supported
    'off_underline': '\033[24m',
    'off_slow': '\033[25m',
    'off_fast': '\033[26m',      #not well supported
    'off_inverse': '\033[27m',
    'off_hide': '\033[28m',

    'black': '30',
    'red':'31',
    'green': '32',
    'yellow': '33',
    'blue': '34',
    'magenta': '35',
    'cyan': '36',
    'white': '37',

    'backblack':'40',
    'backred':'41',
    'backgreen': '42',
    'backyellow': '43',
    'backblue': '44',
    'backmagenta': '45',
    'backcyan': '46',
    'backwhite': '47',

    'bright_black' : '90',
    'bright_red' : '91',
    'bright_green' : '92',
    'bright_yellow': '93',
    'bright_blue' : '94',
    'bright_magenta' : '95',
    'bright_cyan' : '96',
    'bright_white' : '97',

    'back_bright_black': '100',
    'back_bright_red': '101',
    'back_bright_green': '102',
    'back_bright_yellow': '103',
    'back_bright_blue': '104',
    'back_bright_magenta': '105',
    'back_bright_cyan': '106',
    'back_bright_white': '107',

    #'nc': '\033[0m', # No Color
    # now define duplicates
    VMode.FATAL: '->red',
    VMode.ERROR: '->red',
    VMode.NORMAL: '->white',
    VMode.WARN: '->yellow',
    VMode.INFO: '->blue',
    VMode.DEBUG: '->underline'
})

def is_verbose(environment, verbose):
    """ True if the environment is in verbose mode; Can print in verbose mode """
    return verbose.value <= environment.get("verbose", VMode.WARN).value

def cprint(color:str, content:str, environment:dict=None, verbose:VMode=VMode.NORMAL):
    """
    Color Print, print out text in the requested color, but respect the verbose
    and color modes of the environment variable.

    Responds to ENV:
    * color - True for color (default), False for standard
    * verbose - print verbose mode

    Parameters:
    * color - terminal color code
    * content - text to print out
    * environment - optional environment dictionary
    * verbose - print verbose mode for content (default is NORMAL)

    Return: None
    """
    if environment is None:
    	environment = {}
    if is_verbose(environment, verbose):
        if environment.get("color", True):
            print ("{}{}{}".format(color, content, tcode.nc))
        else:
            print ("{}".format(content))

def encoder(color, content):
    return "{}{}{}".format(color, content, tcode.nc)

# decorators

def black(foo):
    return lambda c : encoder(tcode.black, foo(c))

def red(foo):
    return lambda c : encoder(tcode.red, foo(c))

def black_green(foo):
    color = tcode.full("black", "backgreen")
    return lambda c : encoder(color, foo(c))

def green(foo):
    return lambda c : encoder(tcode.green, foo(c))

def blue(foo):
    return lambda c : encoder(tcode.blue, foo(c))

def bold(foo):
    return lambda c : encoder(tcode.bold, foo(c))

def underline(foo):
    return lambda c : encoder(tcode.underline, foo(c))

def link(link, text):
    return '\033]8;;{}\a{}\033]8;;\a'.format(link, text)

def print_red(function):
    def inner(*args):
         ret = function(*args)
         cprint(tcode.red, ret)
         return ret
    return inner

def print_green(function):
    def inner(*args):
         ret = function(*args)
         cprint(tcode.green, ret)
         return ret
    return inner

def print_blue(function):
    def inner(*args):
         ret = function(args)
         cprint(tcode.blue, ret)
         return ret
    return inner

def command(code):
    print (code, end='')

def vcprint(verbose:VMode, content:str, environment:dict=None):
    """
    Verbose Color Printing:
    Decided what color to print out for the user, based on verbose level

    Parameters:
    * verbose - level for print context
    * content - text to print out
    * environment - application settings
    """
    cprint (tcode.get(verbose, tcode.white), content, environment, verbose)

def cmd_clear_screen():
    print('\033[2J', end='')

def cmd_clear_line():
    print('\033[2K', end='')

def cmd_clear_end_line():
    print('\033[K', end='')

def cmd_save_position():
    print('\033[s', end='')

def cmd_restore_position():
    print('\033[u', end='')

def cmd_move(num, direction):
    direction = direction.upper()
    match direction:
        case "UP":
            direction = "A"
        case "DOWN":
            direction = "B"
        case "RIGHT":
            direction = "C"
        case "LEFT":
            direction = "D"
    print('\033[{}{}'.format(num, direction), end='')

def cmd_move_to(line, column):
    print('\033[{};{}H'.format(line, column), end='')
