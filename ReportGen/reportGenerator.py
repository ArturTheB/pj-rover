# -*- coding: iso-8859-1 -*-
''' This class uses libraries for creating a .pdf '''

# filename = 'Modelling_2.xml'
##############################################################################
from pdfGen import *
from xmlExtract import *

##############################################################################
if __name__ == "__main__":
        # Initialize pdfGen
    # Initialize pdfGen
    pdfGen = PdfGen()

    # Initialize document
    styleSheet = getSampleStyleSheet()# get a sample style sheet
    my_doc = SimpleDocTemplate('report.pdf') # write to a file called report.pdf, associated with SimpleDocTemplate
    flowables = [] # list of elements/content that we want to add to the pdf

    # Initialize xmlExtract
    xml = XMLextract()
    xml.getPackages()
    xml.getDiagrams()

    # Create paragraphs
    title = Paragraph("Report Generator", styleSheet['Title'])
    # Append .pdf's content
    flowables.append(title)
    try:
        for k, v in xml.packages.items():
            package = Package(k, v)
            flowables.append(Paragraph("Package: " + str(k), styleSheet['Heading1']))
            package.getDiagramsForPackage(xml.diagrams)
            for diag in package.diagrams:
                if diag.type == 'Class Diagram':
                    # Diagram
                    diagram = Diagram(diag.name, diag.handle, diag.type)
                    flowables.append(Paragraph("Diagram: " + str(diagram.name), styleSheet['Heading2']))
                    picture = pdfGen.findPicture(diagram.name)
                    picture = pdfGen.scalePicture(picture)
                    flowables.append(picture)
                    # Classifiers
                    diagram.getClassifiersForDiagram(package.handle)
                    diagram.getAssociations(package.handle)
                    diagram.changeAssociationsStartEndIds(diagram.classifiers, diagram.associations)
                    flowables.append(Paragraph("Use case list", styleSheet['Heading3']))
                    table = pdfGen.createTableClassifier(diagram.classifiers)
                    flowables.append(table)
                    # Associations
                    flowables.append(Paragraph("Association list", styleSheet['Heading3']))
                    table = pdfGen.createTableAssociations(diagram.associations)
                    flowables.append(table)

                if diag.type == 'Activity Diagram':
                    diagram = Diagram(diag.name, diag.handle, diag.type)
                    # Diagram name
                    flowables.append(Paragraph("Diagram: " + str(diagram.name), styleSheet['Heading2']))
                    picture = pdfGen.findPicture(diagram.name)
                    picture = pdfGen.scalePicture(picture)
                    flowables.append(picture)
                    # Activities
                    diagram.getClassifiersForDiagram(package.handle)
                    flowables.append(Paragraph("Activities", styleSheet['Heading3']))
                    table = pdfGen.createTableClassifier(diagram.classifiers)
                    flowables.append(table)
                    #Transitions
                    diagram.getTransitions(diagram)
                    diagram.changeTransitionsStartEndIds(diagram.classifiers, diagram.transitions)
                    flowables.append(Paragraph('Transitions: ', styleSheet['Heading3']))
                    table = pdfGen.createTableTransition(diagram.transitions)
                    flowables.append(table)

                if diag.type == 'Sequence Diagram':
                    diagram = Diagram(diag.name, diag.handle, diag.type)
                    # Diagram name
                    flowables.append(Paragraph("Diagram: " + str(diagram.name), styleSheet['Heading2']))
                    picture = pdfGen.findPicture(diagram.name)
                    picture = pdfGen.scalePicture(picture)
                    flowables.append(picture)
                    # Classifiers
                    diagram.getClassifiersForDiagram(package.handle)
                    flowables.append(Paragraph("Sequences", styleSheet['Heading3']))
                    table = pdfGen.createTableClassifier(diagram.classifiers)
                    flowables.append(table)
                    # Transitions
                    diagram.getMessagesForSequenceDiagram(diag.handle)
                    diagram.changeTransitionsStartEndIds(diagram.classifiers, diagram.messages)
                    flowables.append(Paragraph('Transitions: ', styleSheet['Heading3']))
                    table = pdfGen.createTableTransition(diagram.messages)
                    flowables.append(table)

                if diag.type == 'UseCase Diagram':
                    # Diagram name
                    diagram = Diagram(diag.name, diag.handle, diag.type)
                    flowables.append(Paragraph("Diagram: " + str(diagram.name), styleSheet['Heading2']))
                    picture = pdfGen.findPicture(diagram.name)
                    picture = pdfGen.scalePicture(picture)
                    flowables.append(picture)
                    # Classifiers
                    diagram.getClassifiersForDiagram(package.handle)
                    flowables.append(Paragraph("Use Cases", styleSheet['Heading3']))
                    diagram.getUseCases(package)
                    flowables.append(pdfGen.createTableClassifier(diagram.classifiers))
                    # Generalizations
                    diagram.getGeneralizations(package)
                    diagram.orderGeneralizations()
                    flowables.append(Paragraph("Generalizations", styleSheet['Heading3']))
                    flowables.append(pdfGen.createTableGeneralizations(diagram.generalizations))
                    # Dependencies
                    diagram.getDependencies(package)
                    diagram.orderDependencies()
                    flowables.append(Paragraph("Dependencies", styleSheet['Heading3']))
                    flowables.append(pdfGen.createTableDependencies(diagram.dependencies))

                if diag.type == 'State Machine Diagram':
                    # Diagram name
                    diagram = Diagram(diag.name, diag.handle, diag.type)
                    flowables.append(Paragraph("Diagram: " + str(diagram.name), styleSheet['Heading2']))
                    picture = pdfGen.findPicture(diagram.name)
                    picture = pdfGen.scalePicture(picture)
                    flowables.append(picture)
                    # Classifiers
                    diagram.getClassifiersForDiagram(package.handle)
                    flowables.append(Paragraph("Diagrams states", styleSheet['Heading3']))
                    flowables.append(pdfGen.createTableClassifier(diagram.classifiers))
                    # Transitions
                    diagram.getTransitions(diagram)
                    diagram.changeTransitionsStartEndIds(diagram.classifiers, diagram.transitions)
                    flowables.append(Paragraph('Transitions: ', styleSheet['Heading3']))
                    table = pdfGen.createTableTransition(diagram.transitions)
                    flowables.append(table)
            flowables.append(PageBreak())

    finally:
            # Create document
        my_doc.build(flowables,
                onFirstPage=pdfGen.addPageNumber,
                onLaterPages=pdfGen.addPageNumber,)
