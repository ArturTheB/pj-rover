from xmlExtract import XMLextract

from reportlab.platypus import SimpleDocTemplate #high level components for us to use for pdf contained in a module called platypus
from io import BytesIO # for
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph    # For Paragraph object
from reportlab.platypus import PageBreak    # For PageBreak object
from reportlab.platypus import Table    # For Tables
from reportlab.lib.units import mm

##############################################################################
class PdfGen():
    """ Tools for model generation """
#----------------------------------------------------------------------
    def addPageNumber(self, canvas, doc):
        """ Add the page number """
        page_num = canvas.getPageNumber()
        text = "%s" % page_num
        canvas.drawRightString(200*mm, 20*mm, text)
#----------------------------------------------------------------------
    def createTableUseCase(self, useCaseList):
        """ Add table """

        data = []
        for uc in useCaseList:
            temp = [uc, ""]
            data.append(temp)
        data.insert(0, ['Name', 'Summary'])
        table = Table(data, style=[('FONTSIZE', (0,0), (1, 0), 14, "Bold"),
                                   ('TEXTFONT', (0, 0), (1, 0), 'Times-Bold'),
                                    ('ALIGN', (0,0), (-1, -1), 'CENTER'),
                                    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                                    ('INNERGRID', (0,0), (-1,-1), 0.25, "BLACK"),
                                    ('BOX', (0,0), (-1,-1), 0.25, "BLACK")])

        return table

#----------------------------------------------------------------------
    def createTableClassifier(self, classifierList):
        """ Add table """

        data = []
        for c in classifierList:
            temp = [c, ""]
            data.append(temp)
        data.insert(0, ['Name', 'Summary'])
        table = Table(data, style=[('FONTSIZE', (0,0), (1, 0), 14),
                                   ('TEXTFONT', (0, 0), (1, 0), 'Times-Bold'),
                                    ('ALIGN', (0,0), (-1, -1), 'CENTER'),
                                    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                                    ('INNERGRID', (0,0), (-1,-1), 0.25, "BLACK"),
                                    ('BOX', (0,0), (-1,-1), 0.25, "BLACK")])

        return table

#----------------------------------------------------------------------
    def createTableAction(self, actionList):
        """ Add table """

        data = []
        for ak, av in actionList.items():
            data.append([ak, av])
        data.insert(0, ['Name', 'Type'])
        table = Table(data, style=[('FONTSIZE', (0,0), (1, 0), 10),
                                   ('FONTSIZE', (0,1), (-1, -1), 8),
                                   ('TEXTFONT', (0, 0), (1, 0), 'Times-Bold'),
                                    ('ALIGN', (0,0), (-1, -1), 'CENTER'),
                                    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                                    ('INNERGRID', (0,0), (-1,-1), 0.25, "BLACK"),
                                    ('BOX', (0,0), (-1,-1), 0.25, "BLACK")])

        return table
##############################################################################
if __name__ == "__main__":

        # Initialize functions
    pdfGen = PdfGen()

        # Initialize document
    styleSheet = getSampleStyleSheet()# get a sample style sheet
    my_doc = SimpleDocTemplate('report.pdf') # write to a file called report.pdf, associated with SimpleDocTemplate
    flowables = [] # list of elements/content that we want to add to the pdf

        # Initialize xmlExtract
    xml = XMLextract()
    xml.getPackages()
    xml.getDiagrams()
    xml.getUseCases()
    xml.getClassifiers()

        # Create paragraphs
    title = Paragraph("Report Generator", styleSheet['Title'])
    # paragraph_1 = Paragraph("A title", styleSheet['Heading1'])
    # paragraph_2 = Paragraph("Some normal body text", styleSheet['BodyText'])

        # Build .pdf's content
    flowables.append(title)
    # flowables.append(paragraph_1)
    # flowables.append(PageBreak())
    # flowables.append(paragraph_2)

        # Go through extracted elements and include content to .pdf
    # Make sure xml.packages is not empty
    if bool(xml.packages):
        for k, v in xml.packages.items():
            flowables.append(Paragraph("Package: " + str(k), styleSheet['Heading1']))
            pdfGen.createTable(xml.useCases)
    else:
        flowables.append(Paragraph("Package: Root", styleSheet['Heading1']))
    # Append use case list
        flowables.append(Paragraph("Use case list", styleSheet['Heading2']))
        table = pdfGen.createTableUseCase(xml.useCases) # get table
        flowables.append(table)
    #Append classifier list
        flowables.append(Paragraph("Classifier list", styleSheet['Heading2']))
        table = pdfGen.createTableClassifier(xml.classifiers)
        flowables.append(table)
    # Append diagrams
        # activity diagrams
        flowables.append(PageBreak())
        flowables.append(Paragraph("Activity diagrams", styleSheet['Heading2']))
        for adk, adv in xml.activityDiagrams.items():
            flowables.append(Paragraph(adk, styleSheet['Heading3']))
            flowables.append(Paragraph("Activity Element List: ", styleSheet['Heading4']))
            actions = xml.getActions(adv)
            table = pdfGen.createTableAction(actions)
            flowables.append(table)
        # Class diagrams
        flowables.append(PageBreak())
        flowables.append(Paragraph("Class diagrams", styleSheet['Heading2']))
        for cdk, cdv in xml.classDiagrams.items():
            flowables.append(Paragraph(cdk, styleSheet['Heading3']))
        # Use case diagrams
        flowables.append(PageBreak())
        flowables.append(Paragraph("Use case diagrams", styleSheet['Heading2']))
        for ucdk, ucdv in xml.useCaseDiagrams.items():
            flowables.append(Paragraph(ucdk, styleSheet['Heading3']))


        # Create document
    # my_doc.build(flowables) # Document without page numbers
    my_doc.build(
    flowables,
    onFirstPage=pdfGen.addPageNumber,
    onLaterPages=pdfGen.addPageNumber,)
