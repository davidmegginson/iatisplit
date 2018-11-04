import xml.dom.pulldom
import sys
import argparse

def get_text(element_node):
    return ''.join(node.nodeValue for node in element_node.childNodes if node.nodeType == node.TEXT_NODE)

def run(file_or_url, max, dir=".", start_date=None, end_date=None, humanitarian_only=False):
    doc = xml.dom.pulldom.parse(file_or_url)

    for event, node in doc:
        if event == xml.dom.pulldom.START_ELEMENT and node.tagName == 'iati-activity':
            doc.expandNode(node)
            humanitarian_flag = node.attributes['humanitarian']
            id_nodes = node.getElementsByTagName('iati-identifier')
            title_nodes = node.getElementsByTagName('title')
            date_nodes = node.getElementsByTagName('activity-date')
            print(get_text(id_nodes[0]))
            print(get_text(title_nodes[0].childNodes[0]))
            if humanitarian_flag.nodeValue:
                print("(humanitarian=" + humanitarian_flag.nodeValue + ")")
            for node in date_nodes:
                print('  ', node.attributes['type'].value, node.attributes['iso-date'].value)
            #print(node.toprettyxml(indent='  '))

def main(args):
    argsp = argparse.ArgumentParser(description="Split IATI activity files.")
    argsp.add_argument('--max-activities', '-n', required=True, type=int)
    argsp.add_argument('--start-date', '-s', required=False, default=None)
    argsp.add_argument('--end-date', '-e', required=False, default=None)
    argsp.add_argument('--humanitarian-only', '-H', required=False, default=False, type=bool)
    argsp.add_argument('file_or_url', nargs='?')
    args = argsp.parse_args()
    run(args.file_or_url, args.max_activities)
    

if __name__ == '__main__':
    main(sys.argv)
