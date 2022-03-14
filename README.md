# Shell Wrap
A simple set of tools for writing shell scripts in python

## What this does
Far to much of the world runs on bash shell scripts. A shamefull amount of code, some of which I have contributed to. Shell scripts are just not the best language for most solutions. Python on the other hand is not is a bit more verbose when it comes to directly interacting with commands.

This library hopes to bridge that gap

## Setup

    pip3 install virtualenv
    virtualenv -p python3 shellwrap
    cd shellwrap
    source bin/activate
    
    get clone https://github.com/jceaser/shellwrap.git
    cd shellwrap
    ./run.sh -b -i
    python3 example.py

## Installing

    pip3 install https://github.com/jceaser/shellwrap/releases/download/latest-master/shellwrap-0.0.1-py3-none-any.whl

## Usage

### Printing in color

	from shellwrap import color
	color.cprint(color.tcode.green, "Starting script", env)

### Calling Unix Commands

	from shellwrap import unix
	presult = unix.pipe(['echo', 'one', 'two', 'three'], ['wc', '-m'])

	print(unix.ccurl('-v',
		'-H', 'Header: Value',
		'https://github.com/jceaser/shellwrap.git'))

### Reading Files

	from shellwrap import file
	print(file.read_file('.editorconfig'))

### Interactivity

	from shellwrap import interactivity
	interactive.interactive(env, g=globals())
	interactive.user_commands(handler=process_actions, g=globals())

The function `interactivity()` will start a python shell with the scope of the `globals()` as the global for the session. This means that any public methods in the calling file are public in the session allowing for any of them to be run and interacted with. History is remembered.

The function `user_commands()` is a little different. This ones will prompt the user for commands which are then handled by `process_actions(action=None, env:dict=None)`. This allows the calling function more control over what actions are offered. History is also remembered.

----
Copyright &copy; 2022 Thomas Cherry. This software is declared to be under the BSD license.