# -*- coding: iso-8859-1 -*-
''' This class fetches informations from xml '''
##############################################################################
from lxml import etree

filename = 'Modelling.xml'
#==============================================================================
class XMLextract():
#----------------------------------------------------------------------
    def __init__(self):
        self.tree = etree.parse(filename)
        self.root= self.tree.getroot()

#----------------------------------------------------------------------
    def findAllTags(self, tagName):
        """ This function searches for all tags in document with name in <tagName> """

        allTags = self.root.findall(".//" + str(tagName), self.root.nsmap)

        return allTags

#----------------------------------------------------------------------
    def findTags(self, handle, tagName):
        """ This function searches for all tags in document with name <tagName> starting from tag <handle> """

        tags = handle.findall(".//" + str(tagName), self.root.nsmap)

        return tags
#----------------------------------------------------------------------
    def getAttribute(self, tagHandle, attributeName):
        """ Gets an attribute <attributeName> from tag """

        value = tagHandle.get(attributeName)

        return value

#----------------------------------------------------------------------
    def getPackages(self):
        """ Stores all of packages to self.packages """

        self.packages = {}
        allPackages = self.findAllTags("UML:Package")
        for package in allPackages:
            packageName = self.getAttribute(package, "name")
            if packageName != None:
                self.packages.update({packageName: package}) # key: package Name, value: package handle

#----------------------------------------------------------------------
    def getDiagrams(self):
        """ Stores all diagrams from XML to self.diagrams """

        self.diagrams = {}
        self.activityDiagrams = {}
        self.classDiagrams = {}
        self.useCaseDiagrams = {}
        self.stateMachineDiagrams = {}
        self.sequenceDiagrams = {}

        # Search for Jude diagrams
        allJudes = self.findAllTags("JUDE:Diagram")
        for jude in allJudes:
            judeName = self.getAttribute(jude, "name")
            # Are the names empty?
            if judeName != None:
                self.diagrams.update({judeName : jude})
                if self.getAttribute(jude, "typeInfo") == "UseCase Diagram":
                    self.useCaseDiagrams.update({judeName : jude}) # judeName: Name of diagram, jude: diagram handle
                elif self.getAttribute(jude, "typeInfo") == "Class Diagram":
                    self.classDiagrams.update({judeName : jude})

        #Search for JUDE:ActivityDiagram
        allJudeActivity = self.findAllTags("JUDE:ActivityDiagram")
        for jude in allJudeActivity:
            judeName = self.getAttribute(jude, "name")
            # Are the names empty?
            if judeName != None:
                self.diagrams.update({judeName : jude})
                self.activityDiagrams.update({judeName : jude})

        # Search for JUDE:StateChartDiagram
        allStateJudes = self.findAllTags('JUDE:StateChartDiagram')
        for jude in allStateJudes:
            stateJudeName = self.getAttribute(jude, 'name')
            if stateJudeName != None:
                self.diagrams.update({stateJudeName: jude}) # key: diagram name, value: diagram tag handle
                self.stateMachineDiagrams.update({stateJudeName: jude})

        # Search for JUDE:SequenceDiagram
        allSequenceJudes = self.findAllTags('JUDE:SequenceDiagram')
        for jude in allSequenceJudes:
            sequenceJudeName = self.getAttribute(jude, 'name')
            if sequenceJudeName != None:
                self.diagrams.update({sequenceJudeName: jude})
                self.sequenceDiagrams.update({sequenceJudeName: jude})

#----------------------------------------------------------------------
    def getClassifiers(self):
        """ Stores all of classifiers in self.classifiers. Only Activity and Class diagrams """

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
        """ This function delivers all of actions for activity element list """

        actions = {}
        allTags = self.findTags(handle, "JUDE:ActionStatePresentation")
        for tag in allTags:
            labelName = self.getAttribute(tag, "label")
            if labelName != None:
                actions.update({labelName : "action"})
                # actions.append(labelName)

        return actions
#----------------------------------------------------------------------
# #==============================================================================
class Package(XMLextract):
    #----------------------------------------------------------------------
    def __init__(self, name, handle):
        # XMLextract.__init__(self) # get all attributes of parent class
        super().__init__()
        self.name = name
        self.handle = handle
        self.id = self.getID()

    #----------------------------------------------------------------------
    def getID(self):
        """ Get xmi.id of package <self> """

        id = self.getAttribute(self.handle, "xmi.id")

        return id

    #----------------------------------------------------------------------
    def getDiagramsForPackage(self, allDiagrams):
        ''' Get all diagrams included in the package <self> from dict allDiagrams'''

        self.diagrams = []

        for k, v in allDiagrams.items():
            if self.getAttribute(v, 'typeInfo') == 'Class Diagram':
                tagHandle = self.findTags(v, "UML:Namespace") # unfortunately the "tagHandle" is a list
                if tagHandle: # check if the list is empty
                    tagValue = self.getAttribute(tagHandle[0], "xmi.idref") # don't know why tagHandle is a list
                    if self.getID() == tagValue:
                        self.diagrams.append(Diagram(k, v, 'Class Diagram'))

            elif self.getAttribute(v, 'typeInfo') == 'StateChart Diagram':
                diagIdRefTag = self.findTags(v, "UML:StateMachine") # unfortunately the "tagHandle" is a list
                diagIdRef = self.getAttribute(diagIdRefTag[0], 'xmi.idref')
                stateMachineTagsInPackage = self.findTags(self.handle, 'UML:StateMachine')
                for stateMachineTag in stateMachineTagsInPackage:
                    if self.getAttribute(stateMachineTag, 'xmi.id') == diagIdRef:
                        self.diagrams.append(Diagram(k, stateMachineTag, 'State Machine Diagram'))

            elif self.getAttribute(v, 'typeInfo') == 'Activity Diagram':
                diagIdRefTag = self.findTags(v, 'UML:ActivityGraph')
                diagIdRef = self.getAttribute(diagIdRefTag[0], 'xmi.idref')
                activityDiagramsTagsInPackage = self.findTags(self.handle, 'UML:ActivityGraph')
                for activityTag in activityDiagramsTagsInPackage:
                    if self.getAttribute(activityTag, 'xmi.id') == diagIdRef:
                        self.diagrams.append(Diagram(k, activityTag, 'Activity Diagram'))

            elif self.getAttribute(v, 'typeInfo') == 'Sequence Diagram':
                diagIdRefTag = self.findTags(v, 'UML:Collaboration')
                diagIdRef = self.getAttribute(diagIdRefTag[0], 'xmi.idref') # Get xmi.idref for package searching
                sequenceDiagramsTagsInPackage = self.findTags(self.handle, 'UML:Collaboration') # Find all diagrams' handles in package. I. e. collaborations
                for sequenceTag in sequenceDiagramsTagsInPackage:
                    if self.getAttribute(sequenceTag, 'xmi.id') == diagIdRef:
                        self.diagrams.append(Diagram(k, sequenceTag, 'Sequence Diagram'))

            elif self.getAttribute(v, 'typeInfo') == 'UseCase Diagram':
                diagIdRefTag = self.findTags(v, 'UML:Namespace')
                diagIdRef = self.getAttribute(diagIdRefTag[0], 'xmi.idref')
                if self.getAttribute(self.handle, 'xmi.id') == diagIdRef:
                    self.diagrams.append(Diagram(k, v, 'UseCase Diagram'))

    #----------------------------------------------------------------------
    def getClassifiersForPackage(self, packageHandle):
        ''' Collects all classifiers in package '''

        self.classifiers = []
        allClassClassifiers = self.findTags(packageHandle, "UML:Class")
        for classifier in allClassClassifiers:
            classifierName = self.getAttribute(classifier, "name")
            #Are the names empty?
            if classifierName != None:
                classifierId = self.getAttribute(classifier, 'xmi.id')
                self.classifiers.append(Classifier(classifierName, classifier, 'Classifier', classifierId))
#==============================================================================
class Diagram(Package):
    ''' Class for creating and manipulating with diagrams '''
    #----------------------------------------------------------------------
    def __init__(self, name, handle, type):
        ''' Constructor '''
        super().__init__(name, handle)
        # self.name = name
        # self.handle = handle
        self.type = type

    #----------------------------------------------------------------------
    def getType(self, diagramHandle):

        type = self.getAttribute(diagramHandle, 'typeInfo')

        return type
    #----------------------------------------------------------------------
    def getClassifiersForDiagram(self, packageHandle):
        ''' Fetch all classifiers for diagram '''

        self.classifiers = []

        if self.type == 'State Machine Diagram':
            states = self.findTags(self.handle, 'UML:CompositeState')
            pseudostates = self.findTags(self.handle, 'UML:Pseudostate')
            finalStates = self.findTags(self.handle, 'UML:FinalState')
            for state in states:    # Find states
                stateName = self.getAttribute(state, 'name')
                if stateName != None and stateName != '': # Search for non empty states
                    classifierId = self.getAttribute(state, 'xmi.id')
                    self.classifiers.append(Classifier(stateName, state, 'State', classifierId))
            for pseudostate in pseudostates:
                pseudostateName = self.getAttribute(pseudostate, 'name')
                if pseudostateName != None and pseudostateName !='':
                    pseudostateId = self.getAttribute(pseudostate, 'xmi.id')
                    self.classifiers.append(Classifier(pseudostateName, pseudostate, 'State', pseudostateId))
            for finalState in finalStates:
                finalStateName = self.getAttribute(finalState, 'name')
                if finalStateName != None and finalStateName !='':
                    finalStateId = self.getAttribute(finalState, 'xmi.id')
                    self.classifiers.append(Classifier(finalStateName, finalState, 'State', finalStateId))

        if self.type == 'Class Diagram':
            self.getClassifiersForPackage(packageHandle)
            attributes = []
            for classifier in self.classifiers:
                classifier.type = 'Class'
                classifier.getAttributesForClassifier(classifier.handle)
                classifier.getOperations(classifier.handle)

        if self.type == 'Activity Diagram':
            states = self.findTags(self.handle, 'UML:ActionState')
            pseudostates = self.findTags(self.handle, 'UML:Pseudostate')
            finalStates = self.findTags(self.handle, 'UML:FinalState')
            for state in states:    # Find states
                stateName = self.getAttribute(state, 'name')
                if stateName != None and stateName != '': # Search for non empty states
                    classifierId = self.getAttribute(state, 'xmi.id')
                    self.classifiers.append(Classifier(stateName, state, 'Action State', classifierId))
            for pseudostate in pseudostates:
                pseudostateName = self.getAttribute(pseudostate, 'name')
                if pseudostateName != None and pseudostateName !='':
                    pseudostateId = self.getAttribute(pseudostate, 'xmi.id')
                    self.classifiers.append(Classifier(pseudostateName, pseudostate, 'Action Pseudostate', pseudostateId))
            for finalState in finalStates:
                finalStateName = self.getAttribute(finalState, 'name')
                if finalStateName != None and finalStateName !='':
                    finalStateId = self.getAttribute(finalState, 'xmi.id')
                    self.classifiers.append(Classifier(finalStateName, finalState, 'Action Final State', finalStateId))

        if self.type == 'Sequence Diagram':
            allClassClassifiers = self.findTags(self.handle, "UML:ClassifierRole")
            for classifier in allClassClassifiers:
                classifierName = self.getAttribute(classifier, "name")
                #Are the names empty?
                if classifierName != None:
                    classifierId = self.getAttribute(classifier, 'xmi.id')
                    self.classifiers.append(Classifier(classifierName, classifier, 'Classifier Role', classifierId))

        if self.type == 'UseCase Diagram':
            classifiers = self.findTags(packageHandle, 'UML:Actor')
            for classifier in classifiers:
                if len(classifier): # Check if empty
                    classifierName = self.getAttribute(classifier, 'name')
                    classifierId = self.getAttribute(classifier, 'xmi.id')
                    self.classifiers.append(Classifier(classifierName, classifier, 'Actor', classifierId))

    #----------------------------------------------------------------------
    def getUseCases(self, package):
        ''' Get all use cases from package '''

        self.useCases = []

        allUseCases = self.findTags(package.handle, 'UML:UseCase')
        for useCase in allUseCases:
            if useCase != None:
                useCaseName = self.getAttribute(useCase, 'name')
                useCaseId = self.getAttribute(useCase, 'xmi.id')
                # # Find reference
                # diagIdRef = self.findTags(useCase, 'UML:ModelElement.namespace')
                # diagIdRef = self.findTags(useCase[0], 'UML:Namespace')
                # diagIdRef = self.getAttribute(diagIdRef[0], 'xmi.idref')
                self.useCases.append(Classifier(useCaseName, useCase, 'Use Case', useCaseId))

    #----------------------------------------------------------------------
    def getGeneralizations(self, package):
        ''' Get all generalizations '''

        self.generalizations = []

        allGeneralizations = self.findTags(package.handle, 'UML:Generalization')
        for generalization in allGeneralizations:
            if len(generalization):
                generalizationName = self.findTags(generalization, 'name')
                generalizationId = self.findTags(generalization, 'xmi.id')
                self.generalizations.append(Classifier(generalizationName, generalization, 'Generalization', generalizationId))

        for generalization in self.generalizations:
            generalizationChild = self.findTags(generalization.handle, 'UML:Generalization.child')
            generalizationChild = self.findTags(generalizationChild[0], 'UML:GeneralizableElement')
            generalizationChild = self.getAttribute(generalizationChild[0], 'xmi.idref')

            generalizationParent = self.findTags(generalization.handle, 'UML:Generalization.parent')
            generalizationParent = self.findTags(generalizationParent[0], 'UML:GeneralizableElement')
            generalizationParent = self.getAttribute(generalizationParent[0], 'xmi.idref')
            generalization.child = generalizationChild
            generalization.parent = generalizationParent

    #----------------------------------------------------------------------
    def orderGeneralizations(self):
        ''' Get start and end of dependencies '''

        for useCase in self.useCases:
            for generalization in self.generalizations:
                if generalization.child == useCase.id:
                    generalization.child = useCase.name
                if generalization.parent == useCase.id:
                    generalization.parent = useCase.name
    #----------------------------------------------------------------------
    def getDependencies(self, package):
        ''' Get dependencies for use case diagram '''

        self.dependencies = []
        allDependencies = self.findTags(package.handle, 'UML:Dependency')
        for dependency in allDependencies:
            if dependency != None:
                dependencyName = self.getAttribute(dependency, 'name')
                dependencyId = self.getAttribute(dependency, 'xmi.id')
                self.dependencies.append(Classifier(dependencyName, dependency, 'Dependency', dependencyId))

        for dependency in self.dependencies:
            depStart = self.findTags(dependency.handle, 'UML:Dependency.client')
            depStart = self.findTags(depStart[0], 'JUDE:ModelElement')
            depStart = self.getAttribute(depStart[0], 'xmi.idref')

            depEnd = self.findTags(dependency.handle, 'UML:Dependency.supplier')
            depEnd = self.findTags(depEnd[0], 'JUDE:ModelElement')
            depEnd = self.getAttribute(depEnd[0], 'xmi.idref')

            dependency.start = depStart
            dependency.end = depEnd

    #----------------------------------------------------------------------
    def orderDependencies(self):
        ''' Get start and end of dependencies '''

        for dependency in self.dependencies:
            for useCase in self.useCases:
                if dependency.start == useCase.id:
                    dependency.start = useCase.name
                if dependency.end == useCase.id:
                    dependency.end = useCase.name

    #----------------------------------------------------------------------
    def getTransitions(self, diagram):
        ''' Fetch all transitions for state '''

        self.transitions = []

        if diagram.type == 'State Machine Diagram' or diagram.type == 'Activity Diagram':
            allTransitions = self.findTags(diagram.handle, 'UML:Transition')
            for transition in allTransitions:
                tranName = self.getAttribute(transition, 'name')
                if tranName != None:
                    # Find transition start
                    startTag = self.findTags(transition, 'UML:Transition.source')
                    startTag = self.findTags(startTag[0], 'UML:StateVertex') #
                    startId = self.getAttribute(startTag[0], 'xmi.idref')
                    # Find transition end
                    endTag = self.findTags(transition, 'UML:Transition.target')
                    endTag = self.findTags(endTag[0], 'UML:StateVertex')
                    endId = self.getAttribute(endTag[0], 'xmi.idref')
                    self.transitions.append(Transition(tranName, transition, startId, endId, 'Transition'))

    #----------------------------------------------------------------------
    def changeTransitionsStartEndIds(self, diagramClassifiers, transitions):
        ''' Changes start and end transition IDs to classifiers' names '''

        for classifier in diagramClassifiers:
            for transition in transitions:
                if transition.start == classifier.id:
                    transition.start = classifier.name
                if transition.end == classifier.id:
                    transition.end = classifier.name

    #----------------------------------------------------------------------
    def getAssociations(self, packageHandle):

        self.associations = []

        if self.type == 'Class Diagram':
            allAssociations = self.findTags(packageHandle, 'UML:Association')
            for association in allAssociations:
                ends = self.findTags(association, 'UML:AssociationEnd')
                if ends:
                    owners = []
                    multiplicityLowArr = []
                    multiplicityUpperArr = []
                    for end in ends:
                        owner = self.findTags(end, 'UML:Feature.owner')
                        if owner:
                            owner = self.findTags(owner[0], 'UML:Classifier')
                            owner = self.getAttribute(owner[0], 'xmi.idref')
                            multiplicityLow = self.findTags(end, 'UML:StructuralFeature.multiplicity')
                            multiplicityTag = self.findTags(multiplicityLow[0], 'UML:MultiplicityRange')
                            multiplicityLow = self.getAttribute(multiplicityTag[0], 'lower')
                            multiplicityUpper = self.getAttribute(multiplicityTag[0], 'upper')
                            if multiplicityUpper == '-1':
                                multiplicityUpper = 'infinity'
                            multiplicityLowArr.append(multiplicityLow)
                            multiplicityUpperArr.append(multiplicityUpper)
                            owners.append(owner)
                    if len(owners) == 2:
                        assName = self.getAttribute(association, 'name')
                        self.associations.append(Association(assName,
                                                             association,
                                                             owners[0],
                                                             owners[1],
                                                             'Association',
                                                             multiplicityLowArr[0],
                                                             multiplicityUpperArr[0],
                                                             multiplicityLowArr[1],
                                                             multiplicityUpperArr[1]))
    #----------------------------------------------------------------------
    def changeAssociationsStartEndIds(self, diagramClassifiers, associations):
        ''' Changes start and end transition IDs to classifiers' names '''

        for classifier in diagramClassifiers:
            for ass in associations:
                if ass.end1 == classifier.id:
                    ass.end1 = classifier.name
                if ass.end2 == classifier.id:
                    ass.end2 = classifier.name

    #----------------------------------------------------------------------
    def getMessagesForSequenceDiagram(self, diagramHandle):
        ''' Fetch all operations for diagram '''

        self.messages = []
        allInteraction = self.findTags(diagramHandle, 'UML:Interaction')
        for interaction in allInteraction:
            messageTag = self.findTags(interaction, 'UML:Message')
            if messageTag: # check if the list is empty
                for message in messageTag:
                    mSR = [] # Message Sender, Receiver
                    messageName = self.getAttribute(message, 'name')
                    mSender = self.findTags(message, 'UML:Message.sender')
                    mReceiver = self.findTags(message, 'UML:Message.receiver')
                    if mSender: # Check if empty
                        mSenderId = self.findTags(mSender[0], 'UML:ClassifierRole')
                        mSenderId = self.getAttribute(mSenderId[0], 'xmi.idref')
                        mSR.append(mSenderId)
                    if mReceiver: # Check if empty
                        mReceiverId = self.findTags(mReceiver[0], 'UML:ClassifierRole')
                        mReceiverId = self.getAttribute(mReceiverId[0], 'xmi.idref')
                        mSR.append(mReceiverId)
                    if len(mSR) == 2:
                        self.messages.append(Transition(messageName, message, mSR[0], mSR[1], 'Message'))
#==============================================================================
class UseCase(XMLextract):
    #----------------------------------------------------------------------
    def __init__(self, name, handle, id, refId):
        super().__init__()
        self.name = name
        self.handle = handle
        self.id = id
        self.refId = refId

#==============================================================================
class Classifier(Diagram):
    #----------------------------------------------------------------------
    def __init__(self, name, handle, type, id):
        ''' Constructor '''
        super().__init__(name, handle, type)
        # self.name = name
        # self.handle = handle
        # self.type = type
        self.id = id

    #----------------------------------------------------------------------
    def getAttributesForClassifier(self, classifierHandle):
        ''' Fetch all attributes associated with classifier '''

        self.attributes = []
        allAttributes = self.findTags(classifierHandle, 'UML:Attribute')
        for attribute in allAttributes:
            attributeName = self.getAttribute(attribute, 'name')
            if attributeName != None:
                attrId = self.getAttribute(attribute, 'xmi.id')
                self.attributes.append(Attribute(attributeName, attribute, attrId))

    #----------------------------------------------------------------------
    def getOperations(self, classifierHandle):

        self.operations = []
        allOperations = self.findTags(classifierHandle, 'UML:Operation')
        for operation in allOperations:
            operationName = self.getAttribute(operation, 'name')
            if operationName != None:
                opId = self.getAttribute(operation, 'xmi.id')
                self.operations.append(Operation(operationName, operation, opId))

#==============================================================================
class Transition(Diagram):
    #----------------------------------------------------------------------
    def __init__(self, name, handle, start, end, type):
        super().__init__(name, handle, type)
        # self.name = name
        # self.handle = handle
        # self.type = type
        self.start = start
        self.end = end

#==============================================================================
class Association():
    #----------------------------------------------------------------------
    def __init__(self, name, handle, end1, end2, type, multiplicity1Low, multiplicity1Upper,
                 multiplicity2Low, multiplicity2Upper):
        self.name = name
        self.handle = handle
        self.end1 = end1
        self.end2 = end2
        self.type = type
        self.mul1Low = multiplicity1Low
        self.mul1Upper = multiplicity1Upper
        self.mul2Low = multiplicity2Low
        self.mul2Upper = multiplicity2Upper

    #----------------------------------------------------------------------
#==============================================================================
class Attribute(Classifier):
    #----------------------------------------------------------------------
    def __init__(self, name, handle, id):
        self.name = name
        self.handle = handle
        self.id = id

    #----------------------------------------------------------------------

#==============================================================================
class Operation(Classifier):
    #----------------------------------------------------------------------
    def __init__(self, name, handle, id):
        self.name = name
        self.handle = handle
        self.id = id

##############################################################################
if __name__ == "__main__":
    pass

    # rG = XMLextract()
    # rG.getPackages()
    # rG.getDiagrams()
    #
    # for k, v in rG.packages.items():
    #     print('=============================')
    #     print ('\n\n\tPackage')
    #     print(k)
    #     package = Package(k, v)
    #     package.getDiagramsForPackage(rG.diagrams)
    #     for diag in package.diagrams:
            # if diag.type == 'Class Diagram':
            #     diagram = Diagram(diag.name, diag.handle, diag.type)
            #     print('\n\tDiagram')
            #     print(diagram.name)
            #     diagram.getClassifiersForDiagram(package.handle)
            #     diagram.getAssociations(package.handle)
            #     diagram.changeAssociationsStartEndIds(diagram.classifiers, diagram.associations)
            #     print('Associations: ')
            #     for a in diagram.associations:
            #         print(a.name, a.mul1Low, a.mul1Upper, a.mul2Low, a.mul2Upper)

            # if diag.type == 'Activity Diagram':
            #     diagram = Diagram(diag.name, diag.handle, diag.type)
            #     print('\n\tDiagram')
            #     print(diagram.name)
            #     diagram.getClassifiersForDiagram(package.handle)
            #     print('\nClassifiers')
            #     for act in diagram.classifiers:
            #         print(act.name)
            #     diagram.getTransitions(diagram)
            #     diagram.changeTransitionsStartEndIds(diagram.classifiers, diagram.transitions)
            #     print('\n\tTransitions')
            #     for tran in diagram.transitions:
            #         print('Transition name ', tran.name, ' | Start: ', tran.start, '| End: ', tran.end)

            # if diag.type == 'Sequence Diagram':
            #     diagram = Diagram(diag.name, diag.handle, diag.type)
            #     print('\n\tDiagram')
            #     print(diagram.name)
            #     diagram.getClassifiersForDiagram(package.handle)
            #     diagram.getMessagesForSequenceDiagram(diag.handle)
            #     diagram.changeTransitionsStartEndIds(diagram.classifiers, diagram.messages)
            #     for msg in diagram.messages:
            #         print(msg.name, msg.start, msg.end)

            # if diag.type == 'UseCase Diagram':
            #         diagram = Diagram(diag.name, diag.handle, diag.type)
            #         print('\n\tDiagram')
            #         print(diagram.name)
            #         diagram.getClassifiersForDiagram(package.handle)
            #         diagram.getUseCases(package)
            #         diagram.getGeneralizations(package)
            #         diagram.orderGeneralizations()
            #         diagram.getDependencies(package)
            #         diagram.orderDependencies()

            # if diag.type == 'State Machine Diagram':
            #     # Diagram name
            #     diagram = Diagram(diag.name, diag.handle, diag.type)
            #     print('\n\tDiagram')
            #     print(diagram.name)
            #     # Classifiers
            #     diagram.getClassifiersForDiagram(package.handle)
            #     # print('\nClassifiers')
            #     # for c in diagram.classifiers:
            #     #     print(c.name)
            #     diagram.getTransitions(diagram)
            #     diagram.changeTransitionsStartEndIds(diagram.classifiers, diagram.transitions)
            #     print('\nTransitions:')
            #     for t in diagram.transitions:
            #         print (t.name, t.start, t.end)
