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
        self.diagrams = []
        self.activityDiagrams = []
        self.useCases = []
        self.classifiers = {}

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
    def getDiagrams(self):
        "Stores all diagrams from XML to self.diagrams"

        # Search for Jude diagrams
        allJudes = self.findAllTags("JUDE:Diagram")
        for jude in allJudes:
            judeName = self.getAttribute(jude, "name")
            # Are the names empty?
            if judeName != None:
                self.diagrams.append(judeName)

        #Search for JUDE:ActivityDiagram
        allJudeActivity = self.findAllTags("JUDE:ActivityDiagram")
        for jude in allJudeActivity:
            judeName = self.getAttribute(jude, "name")
            if judeName != None:
                self.diagrams.append(judeName)
                self.activityDiagrams.append(judeName)

#----------------------------------------------------------------------
    def getUseCases(self):
        "Stores all of use cases in self.UseCases"

            # Search for all UML:UseCase
        allUseCase = self.findAllTags("UML:UseCase")
        for useCase in allUseCase:
            useCaseName = self.getAttribute(useCase, "name")
            # Are the names empty?
            if useCaseName != None:
                self.useCases.append(useCaseName)

#----------------------------------------------------------------------
    def getClassifiers(self):
        "Stores all of classifiers in self.classifiers"

            # Search for all UML:Actor
        allActorClassifiers = self.findAllTags("UML:Actor")
        for actorClassifier in allActorClassifiers:
            actorClassifierName = self.getAttribute(actorClassifier, "name")
            #Are the names empty?
            if actorClassifierName != None:
                self.classifiers.update({actorClassifierName: "actor"})

            # Search for all JUDE:ClassifierPresentation
        allClassClassifiers = self.findAllTags("JUDE:ClassifierPresentation")
        for classClassifier in allClassClassifiers:
            classClassifierName = self.getAttribute(classClassifier, "label")
            #Are the names empty?
            if classClassifierName != None:
                self.classifiers.update({classClassifierName: "class"})

# #----------------------------------------------------------------------
#     def getChildren(self, diagramHandle):
#         ""

##############################################################################
if __name__ == "__main__":
    reportGenerator = ReportGenerator()
    # reportGenerator.getDiagrams()
    # reportGenerator.getUseCases()
    reportGenerator.getClassifiers()

    for k, v in reportGenerator.classifiers.items():
        print (k, v)
