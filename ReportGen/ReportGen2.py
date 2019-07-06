# -*- coding: iso-8859-1 -*-
'''This file creates an '''
##############################################################################

from lxml import etree

#----------------------------------------------------------------------
if __name__ == "__main__":
    fileString = 'MarsRoverUseCase.xml'
    tree = etree.parse(fileString)
    root = tree.getroot()
    allJudes = root.findall(".//JUDE:Diagram", root.nsmap)
    for jude in allJudes:
        print(jude.get('name'))
