#!/bin/bash

run_clean()
{
	rm -rf build dist shellwrap.egg-info
}

run_build()
{
	python3 setup.py sdist bdist_wheel
}

run_install()
{
	pip3 install shellwrap-0.0.1-py3-none-any.whl
}

run_test()
{
	python3 -m unittest discover -s ./ -p '*test.py'
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
while getopts "hcbitlu" opt
do
    case ${opt} in
        h) run_help ;;
        c) run_clean ;;
        b) run_build ;;
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
