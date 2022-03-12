#!/usr/bin/env python3

# pylint template.py
# count lines of code with:
# sed -n '/^#cloc-start$/,/^#cloc-end$/p' template.py | cloc - --stdin-name=template.py

#cloc-start

# template modified 2021-09-02

""" template script for future scripts """

#mark - Imports

from enum import Enum   #Creating Enums
import argparse         #command line parsing
import code             #interactive shell
import os               #file handling
import re               #filter in man()
import readline         #interactive shell
import subprocess       #calling unix commands
import sys              #exiting

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
        return self.get(attr, '\033[0m')

tcode = TerminalCode({'red':'\033[0;31m',
    'green': '\033[0;32m',
    'yellow': '\033[0;33m',
    'blue': '\033[0;34m',
    'white': '\033[0;37m',
    'bold': '\033[1m',
    'underline': '\033[4m',
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
    return verbose.value <= environment["verbose"].value

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
    environment = create_environment(environment)
    if is_verbose(environment, verbose):
        if environment["color"]:
            print ("{}{}{}".format(color, content, tcode.nc))
        else:
            print ("{}".format(content))

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

# ######################################
#mark calling unix commands

def call(*command):
    """ take a list of parameters to call on from unix """
    result = subprocess.run(command, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, check=True) # use check?
    return result.stdout.decode('utf-8')

def pipe(*cmd_lists):
    """
    Call multiple commands and pipe the output from one to the next.
    example: pipe(['ps', '-ef'], ['grep', 'Applications'], ['head', '-n', '5'])
    input: a variable number of lists, each list is one command and parameters
    output: the UTF-8 text output of the final command
    """
    pipe_result = None
    for cmd in cmd_lists:
        if pipe_result is None:
            pipe_result = subprocess.run(cmd, check=True, capture_output=True)
        else:
            pipe_result = subprocess.run(cmd, input=pipe_result.stdout,
                capture_output=True, check=True) # use check?
    return pipe_result.stdout.decode('utf-8')

def curl(*flags):
    """ Build a curl command list which can be passed to pipe() or call() """
    cmd = ["curl", "-s", '-A', 'tcherry-script']
    cmd.extend(flags)
    return cmd

def ccurl(*flags):
    """ Run the curl command with some predefined attributes """
    cmd = curl(*flags)
    return call(*cmd)

# ######################################
#mark CMR tools

def cmr_url(environment:dict, endpoint:str, path:str, *options):
    """
    build a CMR url for a given endpoint and path.
    Parameters:
        * environment: dictionary of application instance data
        * endpoint: CMR end point, like search or ingest
        * path: endpoint path
        * options: additional URL parameters
    Return:
        A CMR URL
    """
    # A dictionary of CMR port numbers. - http://localhost:2999/kms
    cmr_ports = {'kms':2999, 'ingest': 3002, 'search':3003}
    environment = create_environment(environment)
    if environment['env'] in ['localhost', 'local']:
        url = 'http://localhost:{}{}'.format(cmr_ports[endpoint], path)
    else:
        url_template = 'https://cmr.{}.earthdata.nasa.gov/{}{}'
        url = url_template.format(environment['env'], endpoint, path)
        url = url.replace(".ops.", ".").replace(".prod.", ".").replace("..", ".")
    return url.format(*options)

# ######################################
#mark Interactive tool

def man(pattern:str=None):
    """ Print out all the doc strings for this scope. """
    world = globals()
    for name in world.keys():
        if not name.startswith('_'):
            display_doc = True if pattern is None else re.match(pattern, name)
            if display_doc:
                obj = world[name]
                if obj is not None and (callable(obj) or hasattr(obj, '__call__')):
                    if obj.__doc__ is not None and len(obj.__doc__.strip())>0:
                        msg = obj.__doc__.strip()
                    else:
                        msg = "No Documentation"
                    print ("## {}()\n\n{}\n--------\n".format(name, msg))

# interactive() calls code.InteractiveConsole.interact() which does not return
# normally, users must call quit() which throws an exception. When this is
# trapped we have a choice to exit the script or continue. True will cause the
# script to exit.
EXIT_AFTER_QUIT=True

def _quit_and_continue():
    """
    Use to overwrite the built in quit() function for use in interactive mode to
    make it easy to quit interactive mode without exiting the entire script.
    """
    # pylint: disable=W0603
    global EXIT_AFTER_QUIT # this is a technique to allow us to capture an exit
    EXIT_AFTER_QUIT = False
    raise SystemExit

def _load_history(file_key:str, file_name:str, environment:dict=None):
    """
    interactive() and user_commands() both initialize history the same way
    Parameters:
        * file_key: environment key to find file name with
        * file_name: backup file name if key does not exists
        * environment: application settings
    Return: Name of file where history was loaded from, need this for saving
    """
    path = create_environment(environment).get(file_key, file_name)
    history_file = os.path.expanduser(path)
    readline.parse_and_bind('tab:complete')
    if os.path.exists(history_file):
        readline.read_history_file(history_file)
    return history_file

def _save_history_maybe_exit(history_file:str, exit_script:bool):
    """ Save readline history and then maybe exit script """
    readline.set_history_length(256)
    readline.write_history_file(history_file)
    if exit_script:
        sys.exit()

def interactive(environment:dict=None):
    """
    Call an interactive interface to this script allowing users to interact with
    the functions and variables directly. using exit will cause this script to
    exit and continue with processing.
    Parameters
        env: environment with application instance data
    """
    # pylint: disable=W0603
    global EXIT_AFTER_QUIT # this is a technique to allow us to capture an exit

    history_file = _load_history("interactive-history",
        ".python-template-interactive-history", environment)

    world = globals()
    world['env'] = environment
    world['quit'] = _quit_and_continue
    console = code.InteractiveConsole(locals=world)
    try:
        console.interact(banner="Interactive mode:\n"
            "    * quit() end interactive mode and continue script\n"
            "    * exit() end script")
    except SystemExit:
        _save_history_maybe_exit(history_file, EXIT_AFTER_QUIT)

def user_commands(handler=None, environment=None):
    """ Enters a readline run loop allowing for input from users with history """
    history_file = _load_history("user-history", ".python-template-user-history", environment)

    running = True
    while running:
        ans = input("Command Mode:\n"
            "    * quit end command mode and continue script\n"
            "    * exit to end script\n")
        if ans in ['quit', 'exit']:
            running = False
        elif ans in ['help', 'man', 'manual']:
            man()
        else:
            if handler is not None and (callable(handler) or hasattr(handler, '__call__')):
                handler(ans, environment)
    _save_history_maybe_exit(history_file, ans=='exit')

#cloc-end

# ##############################################################################
#mark - Script functions - Update these

def create_environment(env=None, color=True, verbose=VMode.NORMAL):
    """
    UPDATE: Add application data as needed
    Create a default environment dictionary
    """
    env = {"color":color, "verbose":verbose} if env is None else env
    return env

def initialize_arguments():
    """ UPDATE: Setup command line parameters """
    parser = argparse.ArgumentParser(description="Tester for CMR-7487")
    parser.add_argument('-t', '--task', help='run some task', action='store_true')
    parser.add_argument('-C', '--color-off', help='no color', action='store_true')
    parser.add_argument('-i', '--interactive', help='enter interactive mode', action='store_true')
    parser.add_argument('-u', '--user', help='enter user mode', action='store_true')
    parser.add_argument('-o', '--option', help='no color')
    parser.add_argument('-v', '--verbose', help='verbose mode', action='store_true')
    parser.add_argument('-vv', '--very-verbose', help='verbose mode', action='store_true')
    args = parser.parse_args()
    return args

def initialize_enviornment(args):
    """ UPDATE: Initialize the Environment variable with app settings """
    environment = create_environment()
    if args.color_off:
        environment["color"] = False
    if args.verbose:
        environment["verbose"]=VMode.WARN
    if args.very_verbose:
        environment["verbose"]=VMode.INFO
    return environment

def process_actions(action=None, env:dict=None):
    """
    UPDATE: Example of how to process user actions
    """
    if action is None:
        return False
    if 'one' in action:
        print("do command 1")
    if 'two' in action:
        print("do command 2")
    if 'some_task' in action:
        some_task(action, env)
    return True

def some_task(option, env:dict=None):
    """ UPDATE: Do some task ; what is the point of this script? """
    cprint(tcode.blue, "Running a task", env)
    cprint(tcode.green, "Results: " + option, env)

# ######################################
#mark - Script entry points

def main():
    """ UPDATE: Main body of the script """

    #House keeping
    args = initialize_arguments()
    env = initialize_enviornment(args)

    if args.interactive:
        interactive(env)
    if args.user:
        user_commands(handler=process_actions, environment=env)

    # Print out some debug info before the script does it's work
    cprint(tcode.blue, args, env, VMode.DEBUG)
    cprint(tcode.blue, call('echo', 'Can talk to UNIX'), env, VMode.DEBUG)

    # Do the work of the script
    option = args.option if args.option else 'default'

    if args.task:
        some_task(option, env)

    # Now demonstrate how to call a URL two different ways
    url = "https://cmr.sit.earthdata.nasa.gov/search/collections?pretty=true"

    # First, make a basic call with curl
    print ("-"*80)
    cprint (tcode.blue, "Basic call to curl", env)
    cprint (tcode.green, ccurl("-H", "Fake:Head", url)[:512], env)

    # Second, use curl-list to call curl and pipe to another command
    print ("-"*80)
    cprint(tcode.blue, "Call curl then pipe to head using curll instead of curl", env)
    cprint(tcode.green, pipe( curl("-H", "Fake:Header", url), ['head', '-n', '8']), env)

    # File testing
    file = '/tmp/test.txt'
    write_file("content from test file", file)
    print(read_file(file))
    os.remove(file)

    # Clean up
    cprint(tcode.blue, "Done", env, VMode.INFO)

if __name__ == "__main__":
    main()
