#coding=UTF8
"""Unit tests for the iatisplit.split module
David Megginson
November 2018

License: Public Domain
"""

import unittest

import iatisplit.split

import os
import xml.dom.minidom

class TestSplit(unittest.TestCase):

    def test_get_element_text_simple(self):
        node = xml.dom.minidom.parseString("<narrative>abcde</narrative>").getElementsByTagName("narrative")[0]
        self.assertEqual("abcde", iatisplit.split.get_element_text(node))

    def test_get_element_text_multiple_nodes(self):
        """Read text across an element-node break."""
        node = xml.dom.minidom.parseString("<narrative>abc<foo/>de</narrative>").getElementsByTagName("narrative")[0]
        self.assertEqual("abcde", iatisplit.split.get_element_text(node))

    def test_get_attribute_simple(self):
        node = xml.dom.minidom.parseString("<narrative xml:lang=\"fr\">abcde</narrative>").getElementsByTagName("narrative")[0]
        self.assertEqual("fr", iatisplit.split.get_attribute(node, "xml:lang"))

    def test_get_attribute_default(self):
        "Return default value if attribute not specified."""
        node = xml.dom.minidom.parseString("<narrative>abcde</narrative>").getElementsByTagName("narrative")[0]
        self.assertEquals("xxxxx", iatisplit.split.get_attribute(node, "xml:lang", "xxxxx"))

    def test_get_activity_dates(self):
        EXPECTED = {
            'start_planned': '2017-01-01',
            'start_actual': '2017-02-01',
            'end_planned': '2017-11-30',
            'end_actual': '2017-12-31'}
        node = _xml_file("iati-activities-simple.xml", "iati-activity")
        activity_dates = iatisplit.split.get_activity_dates(node)
        self.assertEquals(EXPECTED, activity_dates)

def _xml_string(string, element_name=None, element_index=0):
    """Parse an XML string to DOM node(s).
    @param string: a string containing XML markup.
    @see: _xml_search
    """
    return _xml_search(xml.dom.minidom.parseString(string), element_name, element_index)

def _xml_file(filename, element_name=None, element_index=0):
    """Parse an XML string to DOM node(s).
    @param filename: the name of a file, relative to files/ subdirectory.
    @see: _xml_search
    """
    path = os.path.join(os.path.dirname(__file__), "files", filename)
    return _xml_search(xml.dom.minidom.parse(path), element_name, element_index)

def _xml_search(node, element_name=None, element_index=None):
    """Optionally extract nodes from a DOM.
    @param node: the DOM document node (or an element node).
    @param element_name: the XML element name to extract, or None to return the full DOM as supplied.
    @param element_index: the index in the matching nodes to extract, or None to return the full NodeList.
    @returns a node or nodelist, as requested.
    """
    if element_name is not None:
        nodes = node.getElementsByTagName(element_name)
        if element_index is not None:
            return nodes[element_index]
        else:
            return nodes
    else:
        return node
    
