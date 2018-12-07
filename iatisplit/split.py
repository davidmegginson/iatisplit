#coding=UTF8
"""Unit tests for the iatisplit.split module
David Megginson
October 2018

License: Public Domain
"""

import logging, os, re, xml.dom.pulldom


logger = logging.getLogger(__name__)
"""Logger for this module"""


ACTIVITY_DATE_TYPE_CODES = {
    '1': 'start_planned',
    '2': 'start_actual',
    '3': 'end_planned',
    '4': 'end_actual',
}
"""Embed this IATI codelist, since it's critical for operations."""


def split(file_or_url, max, output_dir=".", output_stub=None, start_date=None, end_date=None, humanitarian_only=False):
    """Split an IATI activity report into multiple output documents.
    Start/end date filters use actual dates if present, then fall back to planned dates.
    Uses PullDOM so that it will not exhaust memory with large input documents.
    @param file_or_url: the file path or web URL of the IATI activity report.
    @param max: the maximum number of IATI activities to include in each output document.
    @param output_dir: the path to the output directory (defaults to ".").
    @param start_date: if present, include only activities with a start date on or after this date. Requires ISO format YYYY-MM-DD (e.g. "2018-12-01") (defaults to None).
    @param end_date: if present, include only activities with an end date on or before this date. Requires ISO format YYYY-MM-DD (e.g. "2019-11-30") (defaults to None).
    @param humanitarian_only: if True, include only IATI activities that contain a humanitarian marker (defaults to False).
    """

    doc_counter = 0 # count output documents
    activity_counter = max # force a new output file for the first activity

    # pointer to the top-level iati-activities node
    # (will be reproduced in each output file)
    activities_node = None

    # pointer to the current output stream
    current_output = None

    # Start the XML parser
    events = xml.dom.pulldom.parse(file_or_url)

    output_stub = make_stub(output_stub, file_or_url)

    try:

        # iterate through the document, stopping on every iati-activity element
        for event, node in events:

            # if it's not the start of an element, we don't care
            if event != xml.dom.pulldom.START_ELEMENT:
                continue

            # if it's the top-level iati-activities node, save a copy
            if node.tagName == 'iati-activities':
                activities_node = node
                continue

            # this is where the fun happens
            # we want to parse all of the iati-activity into a single DOM branch,
            # and then print it out to the current file if appropriate; that way,
            # we never hold more than one activity in memory at once.
            elif node.tagName == 'iati-activity':

                # read the rest of this iati-activity element
                events.expandNode(node)

                # get the iati-identifier (for logging)
                iati_id = get_element_text(node.getElementsByTagName('iati-identifier')[0])
                logger.debug("Checking activity %s", iati_id)

                # filter out non-humanitarian activities (if requested)
                if humanitarian_only and not is_humanitarian(node):
                    logger.debug("Skipping activity %s (no humanitarian marker)", iati_id)
                    continue

                # filter out activities not in the date range (if requested)
                if not check_dates_in_range(get_activity_dates(node), start_date, end_date):
                    logger.debug("Skipping activity %s (dates out of range)", iati_id)
                    continue

                # SUCCESS! if we make it to here, then we want to include the activity in our output

                # if the current output document is maxed out, start a new one;
                # otherwise, advance the counter
                if activity_counter >= max:
                    activity_counter = 0
                    doc_counter += 1
                    current_output = end_file(current_output)
                    current_output = start_file(output_dir, output_stub, doc_counter, activities_node)
                else:
                    activity_counter += 1

                # write the activity XML to the current output file and continue
                # XXX Kludge alert! Combining XML output and string appending
                # (to keep indentation neat)
                current_output.write("  " + node.toxml() + "\n")

                continue

    finally:
        # if there's an output file in progress, always close it (even after an exception)
        current_output = end_file(current_output)


def make_stub(output_stub, file_or_url):
    """Figure out the appropriate output-filename stub.
    @param output_stub: the stub explicitly requested by the user (or None).
    @param file_or_url: the filename or URL for the IATI activity file that we're splitting.
    """

    # if the user has already specified one, use it
    if output_stub:
        return output_stub

    # if the file part seems to end with an .xml extension, strip it then go
    result = re.search(r'([^\\/]+)(\.[xX][mM][lL])(\?.*)?$', file_or_url)
    if result:
        return result.group(1)

    # take what looks like the file part
    result = re.search(r'([^\\/]+)(\?.*)?$', file_or_url)
    if result:
        return result.group(1)

    # we give up! use "iatiout"
    return "iatiout"


def start_file(output_dir, output_stub, doc_counter, activities_node):
    """Start a new output file.
    Will open a new XML document and add the start of the iati-activities element.
    @param output_dir: path to the output directory
    @param output_stub: the filename stub for each file (e.g. "iatiout")
    @param doc_counter: current value of the output document counter (1-based)
    @param activities_node: the top-level iati-activities node, for reproduction in each output file
    @returns: a pointer to the open file (for writing individual activities)
    """
    # construct the new filename
    filename = os.path.join(output_dir, "{}.{:04d}.xml".format(output_stub, doc_counter))

    # start the file
    logger.info("Starting output file %s", filename)
    output = open(filename, 'w')

    # write the XML declaration
    output.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")

    # write the iati-activities start tag
    # XXX Kludge alert! Changing an empty element to a start tag by string replacement (blech!).
    # If the Python DOM string representation of an empty element changes in the future,
    # this could break.
    output.write(re.sub(r'/>$', ">\n", activities_node.toxml()))

    # return the new file pointer for writing
    return output


def end_file(current_output):
    """End an output file.
    This is smart enough to do nothing if current_output is None.
    @param current_output: the current file output (or None).
    @returns: None, to represent the closed stream.
    """
    if current_output:
        # write the iati-activities end tag
        current_output.write("</iati-activities>\n")
        # close the output
        current_output.close()
    return None


def is_humanitarian(activity_node):
    """Check if an activity is flagged as humanitarian.
    @param activity_node: the iati-activity DOM element node.
    @returns: True if the humanitarian marker is set on the iati-activity element or any transaction child.
    """
    # first try the iati-activity element
    if get_attribute(activity_node, "humanitarian") == "1":
        return True
    # next, try the transactions
    transaction_nodes = activity_node.getElementsByTagName("transaction")
    for transaction_node in transaction_nodes:
        if get_attribute(transaction_node, "humanitarian") == "1":
            return True
    return False


def check_dates_in_range(activity_dates, start_date=None, end_date=None):
    """Check that an activity's dates fall into the allowed range.
    Prefers the planned date over the actual date when available.
    If the activity dates are missing, returns True
    @param activity_dates: the parsed activity dates.
    @param start_date: the start date in ISO 8601 format (YYYY-MM-DD), or None for no start limit.
    @param end_date: the end date in ISO 8601 format (YYYY-MM-DD), or None for no end limit.
    @returns: True if the activity is in range (or can't be determined).
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
    @returns: a dict of dates found.
    """
    activity_dates = {}
    date_nodes = activity_node.getElementsByTagName('activity-date')
    for node in date_nodes:
        date_type = get_attribute(node, 'type')
        iso_date = get_attribute(node, 'iso-date')
        if iso_date is None:
            logger.error("@iso_date attribute missing")
            continue
        if date_type not in ACTIVITY_DATE_TYPE_CODES:
            logger.error("Unrecognised activity-date/@type %s", date_type)
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
        

# end of module
