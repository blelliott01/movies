from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import PageBreak, TableStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT

def getReportStyles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        'Small', 
        parent=styles['Normal'], 
        fontSize=9)
    )
    styles.add(ParagraphStyle(
        'RightAligned', 
        parent=styles['Small'], 
        alignment=TA_RIGHT)
    )
    styles.add(ParagraphStyle(
        'TopTitle', 
        parent=styles['Title'], 
        alignment=TA_LEFT,
        horizontalAlignment='TOP',
        fontSize=12)
    )    
    return styles

def getSimpleDocTamplate(pdf_filename):
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        topMargin=25,
        bottomMargin=25,
        leftMargin=40,
        rightMargin=10
    )
    return doc