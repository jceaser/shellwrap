from shellwrap import color
from shellwrap import interactive
import argparse

# ######################################
#mark - Setup

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
    environment = {}
    if args.color_off:
        environment["color"] = False

    environment["verbose"] = 0
    if args.verbose:
        environment["verbose"]=1
    if args.very_verbose:
        environment["verbose"]=3
    return environment

# ######################################
#mark - Script tasks

def do_action():
    """ This action is global """
    print ('action')

def some_task(option, env:dict=None):
    """ UPDATE: Do some task ; what is the point of this script? """
    if env is not None and env["verbose"] > 0:
        color.cprint(color.tcode.blue, "Running a task")
    color.cprint(color.tcode.green, "Results: " + option)

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

# ######################################
#mark - Main

def main():
    """ UPDATE: Main body of the script """
    args: argparse.Namespace = initialize_arguments()
    env = initialize_enviornment(args)

    world = globals()
    world['do_action'] = do_action
    world['process_actions'] = process_actions

    # inside the command type "process_actions('some_task')"
    interactive.interactive(env, g=globals())

if __name__ == "__main__":
    main()
