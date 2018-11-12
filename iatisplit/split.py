#coding=UTF8
"""Unit tests for the iatisplit.split module
David Megginson
October 2018

License: Public Domain
"""

import xml.dom.pulldom
import sys
import re
import argparse
import logging

logger = logging.getLogger(__name__)

ACTIVITY_DATE_TYPE_CODES = {
    '1': 'start_planned',
    '2': 'start_actual',
    '3': 'end_planned',
    '4': 'end_actual',
}

def run(file_or_url, max, dir=".", start_date=None, end_date=None, humanitarian_only=False):

    doc_counter = 0
    activity_counter = 0
    
    doc = xml.dom.pulldom.parse(file_or_url)

    print("Starting output file {}".format(doc_counter))
    for event, node in doc:
        if event == xml.dom.pulldom.START_ELEMENT and node.tagName == 'iati-activity':
            if activity_counter >= max:
                activity_counter = 0
                doc_counter += 1
                print("Starting output file {}".format(doc_counter))
            else:
                activity_counter += 1

            doc.expandNode(node)
            humanitarian_flag = node.attributes.get('humanitarian')
            id_nodes = node.getElementsByTagName('iati-identifier')
            title_nodes = node.getElementsByTagName('title')
            date_nodes = node.getElementsByTagName('activity-date')
            print('  ', get_element_text(id_nodes[0]))
            print('  ', get_element_text(title_nodes[0].childNodes[0]))
            if humanitarian_flag and humanitarian_flag.nodeValue:
                print("  (humanitarian=" + humanitarian_flag.nodeValue + ")")

            if start_date or end_date:
                activity_dates = {}
                for node in date_nodes:
                    activity_dates[node.attributes['type'].value] = node.attributes['iso-date'].value
                if start_date and ("1" in activity_dates or "2" in activity_dates):
                    if not (activity_dates.get("1") <= start_date or activity_dates.get("2") <= start_date):
                        continue
                print(activity_dates)
                
            #print(node.toprettyxml(indent='  '))

def get_activity_dates(activity_node):
    """Extract all of the dates in an IATI activity element.
    @param activity_node: the iati-activity DOM element node.
    @returns:
    """
    activity_dates = {}
    date_nodes = activity_node.getElementsByTagName('activity-date')
    for node in date_nodes:
        date_type = get_attribute(node, 'type')
        iso_date = get_attribute(node, 'iso-date')
        if iso_date is None:
            logger.warn("@iso_date attribute missing")
            continue
        if date_type not in ACTIVITY_DATE_TYPE_CODES:
            continue
        activity_dates[ACTIVITY_DATE_TYPE_CODES[date_type]] = iso_date
    return activity_dates
            
def get_attribute(element_node, attribute_name, default_value=None):
    """Extract an attribute value from an element node.
    Does not fail if the attribute isn't present.
    @param element_node: the DOM element node containing the attribute.
    @param attribute_name: the name of the attribute.
    @param default_value: the value to return if the attribute is unspecified.
    @returns: the attribute value, or default_value (None) if it is unspecified.
    """
    node = element_node.attributes.get(attribute_name)
    if node:
        return node.value
    else:
        return default_value
        
def get_element_text(element_node):
    """Extract and concatenate all text from an element node (but not its descendants).
    @param element_node: the XML element containing the text
    @returns: all of the text from the node, concatenated into a single string.
    """
    return ''.join(node.nodeValue for node in element_node.childNodes if node.nodeType == node.TEXT_NODE)

