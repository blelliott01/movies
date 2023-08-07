import os
import csv
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from criterionReportQuery import getQuery
from databaseUtils import connect

conn = connect()
cursor = conn.cursor()
cursor.execute(getQuery())
data = cursor.fetchall()

# Close the database connection
conn.close()

downloads_folder = os.path.expanduser('~/Downloads')
pdf_filename = os.path.join(downloads_folder, 'movie_report.pdf') 
csv_filename = os.path.join(downloads_folder, 'movie_report.csv')

# Export data to CSV
with open(csv_filename, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['title', 'spine'])
    csv_writer.writerows(data)

doc = SimpleDocTemplate(
    pdf_filename, 
    pagesize=letter,
    topMargin=25,
    bottomMargin=25,
    leftMargin=50,
    rightMargin=50
)

# Create a list for the table data
table_data = [['Title', 'Index']]
table_data.extend(data)

# Create the table
table_width = doc.width - doc.leftMargin - doc.rightMargin
column_widths = [table_width * 0.9, table_width * 0.1]

# Create the table with the calculated column widths
table = Table(table_data, colWidths=column_widths)

# Set table style
""" style = TableStyle([
    ('BACKGROUND',      (0, 0), (-1, 0), colors.white),
    ('TEXTCOLOR',       (0, 0), (-1, 0), colors.black),
    ('ALIGN',           (0, 0), (-1, 0), 'LEFT'),
    # ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('TOPPADDING',      (0, 0), (-1, 0), 2),
    ('LEFTPADDING',     (0, 0), (-1, 0), 2),
    ('RIGHTPADDING',    (0, 0), (-1, 0), 2),
    ('BOTTOMPADDING',   (0, 0), (-1, 0), 2),
    # ('GRID', (0, 0), (-1, 0), colors.lightgrey)
])

table.setStyle(style) """

# Build the PDF document
elements = [table]

# Create a custom-styled header with indentation
stylesheet = getSampleStyleSheet()
header_style = stylesheet['Heading1']
header_style.leftIndent = 50

header = Paragraph('<b>Criterion Collection</b>', header_style)

# Build the PDF document
elements = [header, table]  # Add the header before the table

doc.build(elements)

print(f"PDF report saved to {pdf_filename}")
print(f"CSV data exported to {csv_filename}")
