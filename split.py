import xml.dom.pulldom
import sys

LIMIT = 5

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
