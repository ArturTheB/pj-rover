# -*- coding: iso-8859-1 -*-

import xml.etree.ElementTree as ET

class ReportGen(self):
    

#----------------------------------------------------------------------
if __name__ == "__main__":
    fileString = 'MarsRoverUseCase.xml'
    tree = ET.parse('MarsRoverUseCase.xml')
    root = tree.getroot()
    for elem in root:
        print("Child of root element " + str(elem))
        for subelem in elem:
            print("Subelements: " + str(subelem))
        print("\n")
