import xml.dom.pulldom
import sys
import re
import argparse

def get_text(element_node):
    return ''.join(node.nodeValue for node in element_node.childNodes if node.nodeType == node.TEXT_NODE)

def run(file_or_url, max, dir=".", start_date=None, end_date=None, humanitarian_only=False):

    print(start_date)
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
            print('  ', get_text(id_nodes[0]))
            print('  ', get_text(title_nodes[0].childNodes[0]))
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

def main(args):

    def parse_date(s):
        if re.match('^\d{4}-\d{2}-\d{2}$', s):
            return s
        else:
            raise Exception("Bad date format: {}".format(s))
    
    argsp = argparse.ArgumentParser(description="Split IATI activity files.")
    argsp.add_argument('--max-activities', '-n', required=True, type=int)
    argsp.add_argument('--start-date', '-s', required=False, default=None, type=parse_date)
    argsp.add_argument('--end-date', '-e', required=False, default=None, type=parse_date)
    argsp.add_argument('--humanitarian-only', '-H', required=False, default=False, type=bool)
    argsp.add_argument('file_or_url', nargs='?')
    args = argsp.parse_args()
    run(args.file_or_url, args.max_activities, None, args.start_date, args.end_date, args.humanitarian_only)
    

if __name__ == '__main__':
    main(sys.argv)
