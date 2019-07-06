# -*- coding: iso-8859-1 -*-
'''This file creates an '''
##############################################################################
from lxml import etree

filename = 'MarsRoverUseCase.xml'

#==============================================================================
class ReportGenerator():
#----------------------------------------------------------------------
    def __init__(self):
        self.tree = etree.parse(filename)
        self.root= self.tree.getroot()
        self.models = []

#----------------------------------------------------------------------
    def findAllTags(self, tagName):
        "This function searches for all tags with name in <tagName>"

        allTags = self.root.findall(".//" + str(tagName), self.root.nsmap)

        return allTags

#----------------------------------------------------------------------
    def getAttribute(self, tagHandle, attributeName):
        "Gets an attribute <attributeName> from tag"

        value = tagHandle.get(attributeName)

        return value

#----------------------------------------------------------------------
if __name__ == "__main__":
    reportGenerator = ReportGenerator()

        # Search for Jude diagrams
    allJudes = reportGenerator.findAllTags("JUDE:Diagram")
    for jude in allJudes:
        judeName = reportGenerator.getAttribute(jude, "name")
        # Are the names empty?
        if judeName != None:
            reportGenerator.models.append(judeName)

        #Search for JUDE:ActivityDiagram
    allJudeActivity = reportGenerator.findAllTags("JUDE:ActivityDiagram")
    for jude in allJudeActivity:
        judeName = reportGenerator.getAttribute(jude, "name")
        if judeName != None:
            reportGenerator.models.append(judeName)
