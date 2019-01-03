#!/usr/bin/python

from setuptools import setup
import sys

if sys.version_info < (3,):
    raise RuntimeError("iatisplit requires Python 3 or higher")

setup(
    name='iatisplit',
    version="0.3",
    description='Split International Aid Transparency Initiative (IATI) XML activity files.',
    long_description="""Parsing very-large XML files into an in-memory DOM can cause a memory-usage
explosion that shuts down even a large server. This streaming library is optimised to handle very 
large IATI activity reports and split them into smaller XML documents that a system can import
individually. It can load the IATI activity reports either from a local file or direct download
from a (public) URL. Memory usage is relatively constant regardless of the source-file size, so it 
is entirely reasonable to process 100+ MB XML files, even on a resource-constrained system. 
Output goes into a user-specified directory.""",
    author='David Megginson',
    author_email='contact@megginson.com',
    install_requires=['requests'],
    packages=['iatisplit'],
    test_suite='tests',
    entry_points = {
        "console_scripts": [
            "iatisplit = iatisplit.__main__:exec"
        ]
    }
)
