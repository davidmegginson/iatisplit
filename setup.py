#!/usr/bin/python

from setuptools import setup
import sys

if sys.version_info < (3,):
    raise RuntimeError("iatisplit requires Python 3 or higher")

setup(
    name='iatisplit',
    version="0.1",
    description='Split International Aid Transparency Initiative (IATI) XML activity files.',
    author='David Megginson',
    author_email='contact@megginson.com',
    install_requires=[''],
    packages=['iatisplit'],
    test_suite='tests',
    entry_points = {
        "console_scripts": [
            "iatisplit = iatisplit.__main__:exec"
        ]
    }
)
