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
    if args.verbose:
        environment["verbose"]=VMode.WARN
    if args.very_verbose:
        environment["verbose"]=VMode.INFO
    return environment

# ######################################
#mark - Script tasks

def do_action():
    """ This action is global """
    print ('action')

def some_task(option, env:dict=None):
    """ UPDATE: Do some task ; what is the point of this script? """
    color.cprint(color.tcode.blue, "Running a task", env)
    color.cprint(color.tcode.green, "Results: " + option, env)

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
    args = initialize_arguments()
    env = initialize_enviornment(args)

    world = globals()
    world['do_action'] = do_action
    world['process_actions'] = process_actions

    color.cprint(color.tcode.green, "Starting script", env)

    if args.interactive:
        interactive.interactive(env, g=globals())
    if args.user:
        interactive.user_commands(handler=process_actions, environment=env, g=globals())

    color.cprint(color.tcode.red, "ending", env)

if __name__ == "__main__":
    main()
