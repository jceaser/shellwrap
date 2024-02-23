#!/bin/bash

run_init()
{
  pip3 install build
}

run_clean()
{
	rm -rf build dist shellwrap.egg-info
}

run_build()
{
	#python3 setup.py sdist bdist_wheel
	python3 -m build # the new way
}

run_install()
{
	pip3 install dist/shellwrap-0.0.2-py3-none-any.whl
}

run_test()
{
	#python3 -m unittest discover -s ./test -p 'test*.py'
	python3 -m unittest discover
}

run_lint()
{
	pylint shellwrap
	
	#pylint *.py shellwrap \
    #    --disable=duplicate-code \
    #    --extension-pkg-allow-list=math \
    #    --ignore-patterns=".*\.md,.*\.sh,.*\.html,pylintrc,LICENSE,build,dist,tags,shellwrap.egg-info"
}

# Process the command line arguments
while getopts "hcbIitlu" opt
do
    case ${opt} in
        h) run_help ;;
        c) run_clean ;;
        b) run_build ;;
        I) run_init ;;
        i) run_install ;;
        t) run_test ;;
        l) run_lint ;;
        
        u) pip3 uninstall shellwrap ;;
        v) set_version $OPTARG ;;
        *) help ; exit ;;
    esac
done

# default, no options given, run these tasks
if [[ $# -eq 0 ]] ; then
    run_lint
    run_test
fi
