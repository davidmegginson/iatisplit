#coding=UTF8
"""
Unit tests for the iatisplit.split module
David Megginson
November 2018

License: Public Domain
"""

import unittest

import iatisplit.split

import os
import xml.dom.minidom

class TestSplit(unittest.TestCase):

    def test_get_text_simple(self):
        dom = xml.dom.minidom.parseString("<narrative>abcde</narrative>")
        self.assertEqual("abcde", iatisplit.split.get_text(dom.getElementsByTagName("narrative")[0]))

    def test_get_text_multiple_nodes(self):
        dom = xml.dom.minidom.parseString("<narrative>abc<foo/>de</narrative>")
        self.assertEqual("abcde", iatisplit.split.get_text(dom.getElementsByTagName("narrative")[0]))

def read_xml(filename):
    """Read a test XML file and return a miniDOM"""
    path = os.path.join(os.path.dirname(__file__), "files", filename)
    return xml.dom.minidom.parse(path)

