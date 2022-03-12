from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Scripting Tools'
LONG_DESCRIPTION = 'A set of tools to make it easy to write unix scripts'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="shellwrap",
        version=VERSION,
        author="Thomas Cherry",
        author_email="thomas.cherry@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that
        # needs to be installed along with your package. Eg: 'caer'

        keywords=['python', 'shell', 'wrapper', 'shellwrap'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
