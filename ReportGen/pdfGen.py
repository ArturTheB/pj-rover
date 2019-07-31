# -*- coding: iso-8859-1 -*-
''' This class uses libraries for creating a .pdf '''

# from xmlExtract import XMLextract

from reportlab.platypus import SimpleDocTemplate #high level components for us to use for pdf contained in a module called platypus
from io import BytesIO # for
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph    # For Paragraph object
from reportlab.platypus import PageBreak    # For PageBreak object
from reportlab.platypus import Table    # For Tables
from reportlab.lib.units import mm

from pathlib import Path
import os, glob
from svglib.svglib import svg2rlg # for appending with SVGs to .pdf

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
    def findPicture(self, diagramName):
        ''' Finds Picture according to diagram '''

        drawing = None # Placeholder

        for root, dirs, files in os.walk('Pictures'):
            for file in files:
                if file.endswith(".svg") and file == (diagramName + '.svg'):
                    path = os.path.join(root, file)
                    # print(path)
                    drawing = svg2rlg(os.path.join(root, file))

        return drawing
#----------------------------------------------------------------------
    def scalePicture(self, drawing):
        """
        Scale a reportlab.graphics.shapes.Drawing()
        object while maintaining the aspect ratio
        """
        setWidth = 450.0
        scale = setWidth/drawing.width
        scaling_x = scale
        scaling_y = scale

        drawing.width = drawing.width * scaling_x
        drawing.height = drawing.height * scaling_y
        drawing.scale(scaling_x, scaling_y)
        return drawing
#----------------------------------------------------------------------
    def createTableUseCase(self, useCaseList):
        """ Add use case table """

        data = []
        for uc in useCaseList:
            temp = [uc, ""]
            data.append(temp)
        data.insert(0, ['Name', 'Summary'])
        table = Table(data, style=[('FONTSIZE', (0,0), (1, 0), 10, "Bold"),
                                   ('TEXTFONT', (0, 0), (1, 0), 'Times-Bold'),
                                    ('ALIGN', (0,0), (-1, -1), 'CENTER'),
                                    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                                    ('INNERGRID', (0,0), (-1,-1), 0.25, "BLACK"),
                                    ('BOX', (0,0), (-1,-1), 0.25, "BLACK")])

        return table

#----------------------------------------------------------------------
    def createTableGeneralizations(self, generalizationList):
        ''' Get attributes from generalizations '''

        data = []
        for g in generalizationList:
            temp = [g.name, g.type, g.child, g.parent]
            data.append(temp)
        data.insert(0, ['Name', 'Type', 'Child', 'Parent'])
        table = Table(data, style=[('FONTSIZE', (0,0), (1, 0), 10, "Bold"),
                                   ('TEXTFONT', (0, 0), (1, 0), 'Times-Bold'),
                                    ('ALIGN', (0,0), (-1, -1), 'CENTER'),
                                    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                                    ('INNERGRID', (0,0), (-1,-1), 0.25, "BLACK"),
                                    ('BOX', (0,0), (-1,-1), 0.25, "BLACK")])

        return table

#----------------------------------------------------------------------
    def createTableDependencies(self, dependencyList):
        ''' Get attributes from generalizations '''

        data = []
        for d in dependencyList:
            temp = [d.name, d.type, d.start, d.end]
            data.append(temp)
        data.insert(0, ['Name', 'Type', 'Start', 'End'])
        table = Table(data, style=[('FONTSIZE', (0,0), (1, 0), 10, "Bold"),
                                   ('TEXTFONT', (0, 0), (1, 0), 'Times-Bold'),
                                    ('ALIGN', (0,0), (-1, -1), 'CENTER'),
                                    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                                    ('INNERGRID', (0,0), (-1,-1), 0.25, "BLACK"),
                                    ('BOX', (0,0), (-1,-1), 0.25, "BLACK")])

        return table
#----------------------------------------------------------------------
    def createTableAssociations(self, associationList):

        data = []
        for a in associationList:
            temp = [a.name, a.type, a.end1, str(a.mul1Low) + ' ... ' + str(a.mul1Upper), a.end2, str(a.mul2Low) + ' ... ' + str(a.mul2Upper)]
            data.append(temp)
        data.insert(0, ['Name', 'Type', 'Ass. start', 'Multiplicity low ... high', 'Ass. end', 'Multiplicity low ... high'])
        table = Table(data, style=[#('FONTSIZE', (0,0), (1, 0), 14, "Bold"),
                                   #('TEXTFONT', (0, 0), (1, 0), 'Times-Bold'),
                                    ('ALIGN', (0,0), (-1, -1), 'CENTER'),
                                    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                                    ('INNERGRID', (0,0), (-1,-1), 0.25, "BLACK"),
                                    ('BOX', (0,0), (-1,-1), 0.25, "BLACK")])

        return table

# ----------------------------------------------------------------------
    def createTableTransition(self, transitionList):

        data = []
        for t in transitionList:
            temp = [t.name, t.type, t.start, t.end]
            data.append(temp)
        data.insert(0, ['Name', 'Type', 'Transition start', 'Transition end'])
        table = Table(data, style=[('FONTSIZE', (0,0), (-1, -1), 9),
                                   #('TEXTFONT', (0, 0), (1, 0), 'Times-Bold'),
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
            temp = [c.name, c.type]
            data.append(temp)
        data.insert(0, ['Name', 'Type'])
        table = Table(data, style=[('FONTSIZE', (0,0), (1, 0), 10),
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

    pass
