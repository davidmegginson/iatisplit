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
            if humanitarian_flag and humanitarian_flag.nodeValue:
                print("  (humanitarian=" + humanitarian_flag.nodeValue + ")")

            if start_date or end_date:
                activity_dates = get_activity_dates(nodes)
                if start_date and ("start_planned" in activity_dates or "start_actual" in activity_dates):
                    if not (activity_dates.get("start_planned") <= start_date or activity_dates.get("start_actual") <= start_date):
                        continue
                if end_date and ("end_planned" in activity_dates or "end_actual" in activity_dates):
                    if not (activity_dates.get("end_planned") >= start_date or activity_dates.get("end_actual") >= start_date):
                        continue
                print(activity_dates)
                
            #print(node.toprettyxml(indent='  '))

def check_dates_in_range(activity_dates, start_date=None, end_date=None):
    """Check that an activity's dates fall into the allowed range.
    Prefers the planned date over the actual date when available.
    If the activity dates are missing, returns True
    @param activity_dates: the parsed activity dates.
    @param start_date: the start date in ISO 8601 format (YYYY-MM-DD), or None for no start limit.
    @param end_date: the end date in ISO 8601 format (YYYY-MM-DD), or None for no end limit.
    @returns: True if the activity is in range (or can't be determined).
    @see: get_activity_dates
    """
    if start_date:
        if "end_actual" in activity_dates:
            if activity_dates["end_actual"] <= start_date:
                return False
        elif "end_planned" in activity_dates:
            if activity_dates["end_planned"] <= start_date:
                return False
    if end_date:
        if "start_actual" in activity_dates:
            if activity_dates["start_actual"] >= end_date:
                return False
        elif "start_planned" in activity_dates:
            if activity_dates["start_planned"] >= end_date:
                return False
    return True

def get_activity_dates(activity_node):
    """Extract all of the dates in an IATI activity element node.
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

#
# Low-level DOM utility functions
#
            
def get_element_text(element_node):
    """Extract and concatenate all text from an element node (but not its descendants).
    @param element_node: the XML element containing the text
    @returns: all of the text from the node, concatenated into a single string.
    """
    return ''.join(node.nodeValue for node in element_node.childNodes if node.nodeType == node.TEXT_NODE)

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
        
