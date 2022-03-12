import os
import readline
import code
import sys

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
    if environment is None:
    	environment = {}
    path = environment.get(file_key, file_name)
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

def interactive(environment:dict=None, g:dict=None):
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

    for name in g.keys():
    	if not name.startswith('_'):
            world[name] = g[name]

    console = code.InteractiveConsole(locals=world)
    try:
        console.interact(banner="Interactive mode:\n"
            "    * quit() end interactive mode and continue script\n"
            "    * exit() end script")
    except SystemExit:
        _save_history_maybe_exit(history_file, EXIT_AFTER_QUIT)

def user_commands(handler=None, environment=None, g:dict=None):
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
