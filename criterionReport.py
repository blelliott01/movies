import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import TableStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from databaseUtils import connect
from criterionReportQuery import getQuery
from enum import Enum

conn = connect()
cursor = conn.cursor()

cursor.execute("SELECT * FROM owned_or_available_view")

data = cursor.fetchall()

# Close the database connection
conn.close()

# Create the styles
styles = getSampleStyleSheet()

# Define a custom style with a smaller font size
small_style = ParagraphStyle(
    'Small',
    parent=styles['Normal'],
    fontSize=9  # Adjust the font size to make it smaller
)
styles.add(small_style)

# Create a new style for right-aligned cells
right_aligned_style = ParagraphStyle(
    'RightAligned',
    parent=styles['Small'],
    alignment=TA_RIGHT
)
styles.add(right_aligned_style)

            # 0 title,
            # 1 json_extract(omdbData, '$.Director') AS director,
            # 2 year,
            # 3 criterionSpine,
            # 4 shelf,
            # 5 rating,
            # 6 json_extract(omdbData, '$.Runtime') AS runtime,
            # 7 json_extract(omdbData, '$.Country') AS country,
            # 8 json_extract(omdbData, '$.Genre') AS genre,
            # 9 checkedLee,
            # 10 rankTheyShoot

class Cols(Enum):
    TITLE = 0
    DIRECTOR = 1
    YEAR = 2
    RUNTIME = 3
    METACRITIC = 4
    IMDB = 5
    SPINE = 6
    FORMAT = 7
    SHELF = 8
    TSPDT = 9
    TOP100 = 10
    CHECKED = 11

# Create a list of formatted cells
formatted_rows = []
for row in data:
    prefix = ''
    if row[Cols.CHECKED.value] is None:
        prefix = prefix + '>> '
    if row[Cols.SHELF.value] is None:
        prefix = prefix + '$$ '
    if row[Cols.FORMAT.value] == '4K':
        prefix = prefix + '4K '

    if prefix != '' and row[Cols.TSPDT.value] is not None:
        title = f"<b>{prefix}{row[Cols.TITLE.value]}</b>\n"
    elif prefix != '':
        title = f"{prefix}{row[Cols.TITLE.value]}\n"
    else:
        title = f"{row[Cols.TITLE.value]}\n"

    year = f"{row[Cols.YEAR.value]}" if row[Cols.YEAR.value] is not None else 'n/a'
    director = f"{row[Cols.DIRECTOR.value].split(',')[0].strip()}" if row[Cols.DIRECTOR.value] is not None else 'n/a'
    time = f"{row[Cols.RUNTIME.value]}" if row[Cols.RUNTIME.value] is not None else 'n/a'

    if row[Cols.SPINE.value] is not None and row[Cols.SHELF.value] is not None:
        location = f"{row[Cols.SPINE.value]}.{row[Cols.SHELF.value]}"
    elif row[Cols.SPINE.value] is not None:
        location = f"{row[Cols.SPINE.value]}"
    elif row[Cols.SHELF.value] is not None:
        location = f"{row[Cols.SHELF.value]}"
    else:
        location = ''

    info = f"<i>({year}, {director}, {time})</i>\n" 
    if year is None and director is None and time is None:
        info = ''
    
    ratingMC = f"MC: {row[Cols.METACRITIC.value]}% " if row[Cols.METACRITIC.value] is not None else ''
    ratingTS = f"TS: {row[Cols.TSPDT.value]} " if row[Cols.TSPDT.value] is not None else ''

    formatted_row = [
        Paragraph(f"{title}{info}{ratingMC}{ratingTS}", styles['Small']),
        Paragraph(f"{location}", styles['RightAligned']) 
    ]
    formatted_rows.append(formatted_row)

pdf_filename = os.path.join(os.path.expanduser('~/Downloads'), 'movie_report.pdf')

doc = SimpleDocTemplate(
    pdf_filename,
    pagesize=letter,
    topMargin=25,
    bottomMargin=25,
    leftMargin=25,
    rightMargin=25
)

# Create the table
table_width = doc.width - doc.leftMargin - doc.rightMargin
column_widths = [table_width * 0.9, table_width * 0.1]

# Create the table
table = Table(formatted_rows, colWidths=column_widths)  # Specify the column width to match the table width

# Set table style
style = TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), colors.white),
    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('ALIGN', (-1, 0), (-1, -1), 'RIGHT'), 
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, -1), 3),  # Adjust the top padding (reduce the value)
    ('LEFTPADDING', (0, 0), (-1, -1), 3),  # Adjust the left padding (reduce the value)
    ('RIGHTPADDING', (0, 0), (-1, -1), 3),  # Adjust the right padding (reduce the value)
    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),  # Adjust the bottom padding (reduce the value)
])

table.setStyle(style)

# Build the PDF document
elements = [table]

doc.build(elements)

print(f"PDF report saved to {pdf_filename}")