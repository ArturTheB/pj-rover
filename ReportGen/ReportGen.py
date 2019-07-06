# -*- coding: iso-8859-1 -*-
'''This file creates an '''
##############################################################################

import xml.etree.ElementTree as ET


#----------------------------------------------------------------------
if __name__ == "__main__":
    fileString = 'MarsRoverUseCase.xml'
    tree = ET.parse(fileString)
    root = tree.getroot()

    ''' for elem in root:
        print("Child of root element " + str(elem))
        for subelem in elem:
            print("Subelements: " + str(subelem))
        print("\n") '''

    # Find all "JUDE:Diagram" in XML
    allJude = tree.findall("//UML:Model")
