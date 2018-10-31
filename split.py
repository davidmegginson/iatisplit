import xml.dom.pulldom
import sys
import argparse

LIMIT = 5

argsp = argparse.ArgumentParser(description="Split IATI activity files.")
argsp.add_argument('--max-activities', '-n', required=True, type=int)
argsp.add_argument('filenames_or_urls', nargs='*')
args = argsp.parse_args()

print(args.max_activities)
exit()

counter = 0

doc = xml.dom.pulldom.parse(sys.argv[1])

for event, node in doc:
    if event == xml.dom.pulldom.START_ELEMENT and node.tagName == 'iati-activity':
        if counter < LIMIT:
            doc.expandNode(node)
            print(node.toprettyxml(indent='  '))
        else:
            break
        counter += 1
