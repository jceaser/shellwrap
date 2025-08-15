#!/usr/bin/env python3

# pylint template.py
# count lines of code with:
# sed -n '/^#cloc-start$/,/^#cloc-end$/p' template.py | cloc - --stdin-name=template.py

#cloc-start

# template modified 2021-09-02

""" Terminal codes for drawing colors and styles on text """

#mark - Imports

from enum import Enum   #Creating Enums
import re

# ##############################################################################
#mark - Utility functions - Leave these alone

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
            self[key] = value

    def __getattr__ (self, attr):
        """ Allow items to be access with dot notation. """
        color_code = self.get(attr.replace('_', '-'), '\033[0m')
        return color_code

    def escape(self, code) -> str:
        """ Take a TerminalCode and wrap it in terminal escape code. """
        return f'\033[{code}m'

    def full(self, fg, bg):
        fgc = self.get(fg, "0")
        bgc = self.get(bg, "0")
        return f'\033[{fgc};{bgc}m'

#https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences

"""Colors for the following schemas:
* RGB - Red, Green, Blue
* RYG - Red, Yellow, Green
* CMYK - Cyan, Magenta, Yellow, Black
"""
tcode = TerminalCode({'none': '0',
    'bold': '1',
    'faint': '2',
    'italix': '3',    #not well supported
    'underline': '4',
    'slow': '5',
    'fast': '6',      #not well supported
    'inverse': '7',
    'hide': '8',

    'nc': '\033[0m',
    'on-bold': '\033[1m',
    'on-faint': '\033[2m',
    'on-italix': '\033[3m',    #not well supported
    'on-underline': '\033[4m',
    'on-slow': '\033[5m',
    'on-fast': '\033[6m',      #not well supported
    'on-inverse': '\033[7m',
    'on-hide': '\033[8m',

    'off-bold': '\033[21m',
    'off-faint': '\033[22m',
    'off-italix': '\033[23m',    #not well supported
    'off-underline': '\033[24m',
    'off-slow': '\033[25m',
    'off-fast': '\033[26m',      #not well supported
    'off-inverse': '\033[27m',
    'off-hide': '\033[28m',

    'black': '30',
    'red':'31',
    'green': '32',
    'yellow': '33',
    'blue': '34',
    'magenta': '35',
    'cyan': '36',
    'white': '37',

    'back-black':'40',
    'back-red':'41',
    'back-green': '42',
    'back-yellow': '43',
    'back-blue': '44',
    'back-magenta': '45',
    'back-cyan': '46',
    'back-white': '47',

    'bright-black' : '90',
    'bright-red' : '91',
    'bright-green' : '92',
    'bright-yellow': '93',
    'bright-blue' : '94',
    'bright-magenta' : '95',
    'bright-cyan' : '96',
    'bright-white' : '97',

    'back-bright-black': '100',
    'back-bright-red': '101',
    'back-bright-green': '102',
    'back-bright-yellow': '103',
    'back-bright-blue': '104',
    'back-bright-magenta': '105',
    'back-bright-cyan': '106',
    'back-bright-white': '107',

    'clear-screen': '\033[2J',
    'clear-line': '\033[2K',
    'clear-to-end': '\033[K',
    'position-save': '\033[s',
    'position-restore': '\033[u'
})

#emoji: TerminalCode = TerminalCode({':rocket:': '🚀'})
emoji: dict[str,str] = {'none': '',
        'airship':'𐃌',
        'bomb': '💣',
        'chequered': '🏁',
        'degree': '°',
        'firecracker': '🧨',
        'flag': '🏳️',
        'pirate': '🏴‍☠️',
        'platform': '𐁙',
        'post': '🚩',
        'rocket': '🚀',
        'sub': '𐃍',
        'unicorn': '🦄',
        'warn': '⚠️'
}

def cprint(color: str | list[str], content:str):
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

    if isinstance(color, list):
        colors = ";".join(color)
        print(f"\033[{colors}m{content}\033[0m")
    else:
        print ("{}{}{}".format(tcode.escape(color), content, tcode.nc))

def encoder(color: str, content: str):
    """
    Take a color code and text content, either with or without escape code, and return a printable
    escape sequence.
    """
    if color.startswith('\033['):
        return "{}{}{}".format(color, content, tcode.nc)
    else:
        return f"\033[{color}m{content}\033[0m"

def link(link:str, text:str):
    """ Take an html link and link text and return a printable escape sequence. """
    return '\033]8;;{}\a{}\033]8;;\a'.format(link, text)

def colorize(text: str):
    """
    Parse the input text and apply color formatting based on the tags.

    Tags should be in the format :color: where color is the name of the color.
    The :end tag is used to reset the color.

    Example:
    ":red:Hello :green:World:end" will color "Hello" in red and "World" in green.
    """
    # Find all color tags in the text
    tags = re.findall(r':(\w+):', text)

    # Replace each tag with its corresponding ANSI color code
    for tag in tags:
        if tag in tcode:
            text = text.replace(f':{tag}:', f'\033[{tcode[tag]}m')
        elif tag in emoji:
            text = text.replace(f':{tag}:', emoji[tag])
        else:
            # If the tag is not recognized, leave it as is
            pass
    return text

# ##############################################################################
# decorators - experimental

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

# ##############################################################################
# terminal commands

def command(code: str) -> None:
    print (code, end='')

def cmd_clear_screen():
    command(tcode.clear_screen)

def cmd_clear_line():
    command(tcode.clear_line)

def cmd_clear_end_line():
    command(tcode.clear_to_end)

def cmd_save_position():
    command(tcode.position_save)

def cmd_restore_position():
    command(tcode.position_restore)

def cmd_move(num: int, direction: str) -> None:
    direction_normalized: str = direction.upper()
    action: str = ''
    match direction_normalized:
        case "UP":
            action = "A"
        case "DOWN":
            action = "B"
        case "RIGHT":
            action = "C"
        case "LEFT":
            action = "D"
    command(f'\033[{str(num)}{action}')

def cmd_move_to(line: int, column: int):
    command(f'\033[{line};{column}H')
