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
        node = _xml_string("<narrative>abcde</narrative>", "narrative")
        self.assertEqual("abcde", iatisplit.split.get_element_text(node))

    def test_get_element_text_multiple_nodes(self):
        """Read text across an element-node break."""
        node = _xml_string("<narrative>abc<foo/>de</narrative>", "narrative")
        self.assertEqual("abcde", iatisplit.split.get_element_text(node))

    def test_get_attribute_simple(self):
        node = _xml_string("<narrative xml:lang=\"fr\">abcde</narrative>", "narrative")
        self.assertEqual("fr", iatisplit.split.get_attribute(node, "xml:lang"))

    def test_get_attribute_default(self):
        "Return default value if attribute not specified."""
        node = _xml_string("<narrative>abcde</narrative>", "narrative")
        self.assertEquals("xxxxx", iatisplit.split.get_attribute(node, "xml:lang", "xxxxx"))

    def test_is_humanitarian_activity(self):
        # no marker
        node = _xml_string("<iati-activity></iati-activity>", "iati-activity")
        self.assertFalse(iatisplit.split.is_humanitarian(node))
        # marker
        node = _xml_string("<iati-activity humanitarian=\"1\"></iati-activity>", "iati-activity")
        self.assertTrue(iatisplit.split.is_humanitarian(node))

    def test_is_humanitarian_transaction(self):
        # no marker
        node = _xml_string("<iati-activity><transaction/><transaction/><transaction/></iati-activity>", "iati-activity")
        self.assertFalse(iatisplit.split.is_humanitarian(node))
        # marker
        node = _xml_string("<iati-activity><transaction/><transaction humanitarian=\"1\"/><transaction/></iati-activity>", "iati-activity")
        self.assertTrue(iatisplit.split.is_humanitarian(node))


    def test_get_activity_dates(self):
        EXPECTED = {
            'start_planned': '2017-01-01',
            'start_actual': '2017-02-01',
            'end_planned': '2017-11-30',
            'end_actual': '2017-12-31'}
        node = _xml_file("iati-activities-simple.xml", "iati-activity")
        activity_dates = iatisplit.split.get_activity_dates(node)
        self.assertEquals(EXPECTED, activity_dates)

    def test_check_dates_in_range_planned(self):
        DATES = {
            "start_planned": "2018-01-01",
            "end_planned": "2018-12-31",
        }
        # no limits specified
        self.assertTrue(iatisplit.split.check_dates_in_range(DATES, None, None))
        # start date only
        self.assertTrue(iatisplit.split.check_dates_in_range(DATES, "2017-07-01", None))
        self.assertFalse(iatisplit.split.check_dates_in_range(DATES, "2019-07-01", None))
        # end date only
        self.assertTrue(iatisplit.split.check_dates_in_range(DATES, None, "2019-07-01"))
        self.assertFalse(iatisplit.split.check_dates_in_range(DATES, None, "2017-07-01"))
        # overlaps start date
        self.assertTrue(iatisplit.split.check_dates_in_range(DATES, "2017-07-01", "2018-06-30"))
        # overlaps end date
        self.assertTrue(iatisplit.split.check_dates_in_range(DATES, "2018-07-01", "2019-06-30"))
        # no overlap
        self.assertFalse(iatisplit.split.check_dates_in_range(DATES, "2017-01-01", "2017-12-31"))
        self.assertFalse(iatisplit.split.check_dates_in_range(DATES, "2019-01-01", "2019-12-31"))

    def test_check_dates_in_range_actual(self):
        DATES = {
            "start_planned": "2018-01-01",
            "start_actual": "2018-07-01",
            "end_planned": "2018-12-31",
            "end_actual": "2019-06-30",
        }
        # no limits specified
        self.assertTrue(iatisplit.split.check_dates_in_range(DATES, None, None))
        # in range with actual dates but not planned
        self.assertTrue(iatisplit.split.check_dates_in_range(DATES, "2019-01-01", "2019-12-31"))
        # in range with planned dates but not actual
        self.assertFalse(iatisplit.split.check_dates_in_range(DATES, "2017-07-01", "2018-06-30"))

#
# Utility functions
#

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
    
