#!/bin/bash

clean()
{
	rm -rf build dist shellwrap.egg-info
}

build()
{
	python3 setup.py sdist bdist_wheel
}

pip_install()
{
	pip3 install shellwrap.-0.0.1-py3-none-any.whl
}

run_test()
{
	
}

run_lint()
{
	pylint shellwrap
}