# -*- coding: utf-8 -*-

"""
helmdeck turns an Elgato Stream Deck into a mini dashboard and control unit.
"""

import os
from setuptools import setup

base_dir = os.path.dirname(os.path.abspath(__file__))
pkg_name = 'helmdeck'

# adapted from: http://code.activestate.com/recipes/82234-importing-a-dynamically-generated-module/
def pseudo_import( pkg_name ):
    """
    return a new module that contains the variables of pkg_name.__init__
    """
    init = os.path.join( pkg_name, '__init__.py' )

    # remove imports and 'from foo import'
    lines = open(init,'r').readlines()
    lines = filter( lambda l: not l.startswith('from'), lines)
    lines = filter( lambda l: not l.startswith('import'), lines)

    code = '\n'.join(lines)

    import imp
    module = imp.new_module(pkg_name)

    exec(code, module.__dict__)
    return module

# trying to make this setup.py as generic as possible
module = pseudo_import(pkg_name)

setup(
    name=pkg_name,
    packages=[pkg_name],

    install_requires=[
        'click<=9',
        'streamdeck',
        'setproctitle',
    ],

    extras_require = {
        'test': [
            'pytest>=4.3.1',
            'pytest-runner>=4.4',
            'pytest-console-scripts>=0.1.9',
        ],
    },

    entry_points='''
        [console_scripts]
        helmdeck=helmdeck.cli:cli
    ''',

    # metadata for upload to PyPI
    description      = "helmdeck controls an elgato stream deck",
    long_description = __doc__,
    version          = module.__version__,
    author           = module.__author__,
    author_email     = module.__author_email__,
    license          = module.__license__,
    keywords         = "streamdeck".split(),
    url              = module.__url__,

    classifiers      = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        # "Topic :: Software Development :: Documentation",
        # "Topic :: Software Development :: Libraries :: Python Modules",
        # "Topic :: Terminals",
        # "Topic :: Text Processing :: Markup",
        # "Topic :: Utilities",
        ],

    data_files       = [],
)
