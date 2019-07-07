# -*- coding: iso-8859-1 -*-
'''This fetches informations from xml to create a report in .pdf'''
##############################################################################
from lxml import etree

filename = 'RoverOverviewFinal.xml'

#==============================================================================
class ReportGenerator():
#----------------------------------------------------------------------
    def __init__(self):
        self.tree = etree.parse(filename)
        self.root= self.tree.getroot()
        self.packages = {}
        self.diagrams = []
        self.activityDiagrams = {}
        self.classDiagrams = {}
        self.useCaseDiagrams = {}
        self.useCases = []
        self.classifiers = {}

#----------------------------------------------------------------------
    def findAllTags(self, tagName):
        "This function searches for all tags in document with name in <tagName>"

        allTags = self.root.findall(".//" + str(tagName), self.root.nsmap)

        return allTags

#----------------------------------------------------------------------
    def findTags(self, handle, tagName):
        "This function searches for all tags in document with name <tagName> starting from tag <handle>"

        tags = handle.findall(".//" + str(tagName), self.root.nsmap)

        return tags
#----------------------------------------------------------------------
    def getAttribute(self, tagHandle, attributeName):
        "Gets an attribute <attributeName> from tag"

        value = tagHandle.get(attributeName)

        return value

#----------------------------------------------------------------------
    def getPackages(self):
        "Stores all of packages to self.packages"

        allPackages = self.findAllTags("UML:Package")
        for package in allPackages:
            packageName = self.getAttribute(package, "name")
            if packageName != None:
                self.packages.update({packageName: package})

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
                if self.getAttribute(jude, "typeInfo") == "UseCase Diagram":
                    self.useCaseDiagrams.update({judeName : jude}) # judeName: Name of diagram, jude: diagram handle
                elif self.getAttribute(jude, "typeInfo") == "Class Diagram":
                    self.classDiagrams.update({judeName : jude})

        #Search for JUDE:ActivityDiagram
        allJudeActivity = self.findAllTags("JUDE:ActivityDiagram")
        for jude in allJudeActivity:
            judeName = self.getAttribute(jude, "name")
            if judeName != None:
                self.diagrams.append(judeName)
                self.activityDiagrams.update({judeName : jude})

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

#----------------------------------------------------------------------
    def getActions(self, handle):
        "This function delivers all of actions for activity element list"

        actions = {}
        allTags = self.findTags(handle, "JUDE:ActionStatePresentation")
        for tag in allTags:
            labelName = self.getAttribute(tag, "label")
            if labelName != None:
                actions.update({labelName : "action"})
                # actions.append(labelName)

        return actions

#==============================================================================
class Diagram():
#----------------------------------------------------------------------
    def __init__(self, name, type, handle):
        self.name = name # String
        self.type = nameString # String
        self.handle = handle

##############################################################################
if __name__ == "__main__":
    reportGenerator = ReportGenerator()
    reportGenerator.getPackages()
    # reportGenerator.getDiagrams()
    # reportGenerator.getUseCases()
    # reportGenerator.getClassifiers()


    # for k, v in reportGenerator.activityDiagrams.items():
    #     actions = reportGenerator.getActions(v)
    #     print("\n")
    #     print("Actions for diagram " + str(k))
    #     print (actions)
    #     print("\n")
