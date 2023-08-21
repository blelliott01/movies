from operator import itemgetter
import os
from reportlab.platypus import Table, Paragraph
from reportlab.platypus import PageBreak
from enum import Enum, auto
from utilsDatabase import getMovieData
from utilsReport import getReportStyles, getSimpleDocTamplate

class Cols(Enum):
    TITLE = 0
    INFO = auto()
    TSPDT = auto()
    SPINE = auto()
    LOCATION = auto()
    CHECKED = auto()

data = getMovieData("SELECT * FROM location_view")
styles = getReportStyles()

# Create a list of formatted cells
tspdt_rows = []
all_rows = []
for row in data:
    title = f"{row[Cols.TITLE.value]}\n<i>{row[Cols.INFO.value]}</i>\n"

    if row[Cols.TSPDT.value] is not None:
        theyShoot = f"{row[Cols.TSPDT.value]}"
    else:
        theyShoot = ''

    if row[Cols.SPINE.value] is not None:
        location = f"{row[Cols.SPINE.value]} {row[Cols.LOCATION.value]}"
    else:
        location = f"{row[Cols.LOCATION.value]}"

    if row[Cols.CHECKED.value] is None:
        title = f"<b>{title}</b>"
        theyShoot = f"<b>{theyShoot}</b>"
        location = f"<b>{location}</b>"

    formatted_row = [
        Paragraph(f"{title}", styles['Small']),
        Paragraph(f"{theyShoot}", styles['RightAligned']),
        Paragraph(f"{location}", styles['RightAligned']),
        theyShoot
    ]

    all_rows.append(formatted_row)

    if row[Cols.CHECKED.value] is None and row[Cols.TSPDT.value] is not None:
        tspdt_rows.append(formatted_row)

pdf_filename = os.path.join(os.path.expanduser(
    '~/Downloads'), 'location_report.pdf')

# Create the table
doc = getSimpleDocTamplate(pdf_filename)

table_width = doc.width - doc.leftMargin - doc.rightMargin
column_widths = [
    table_width * 0.84,
    table_width * 0.07,
    table_width * 0.09
]

sorted_tspdt_rows = sorted(tspdt_rows, key=itemgetter(3))
sorted_tspdt_rows = [row[:3] for row in sorted_tspdt_rows]
tableChecked = Table(sorted_tspdt_rows, colWidths=column_widths)

all_rows = [row[:3] for row in all_rows]
tableUnchecked = Table(all_rows, colWidths=column_widths)

elements = []
elements.append(tableChecked)
elements.append(PageBreak())
elements.append(tableUnchecked)

doc.build(elements)

print(f"PDF report saved to {pdf_filename}")
