import xml.dom.pulldom
import sys

doc = xml.dom.pulldom.parse(sys.argv[1])

for event, node in doc:
    print(event, node.toxml())
