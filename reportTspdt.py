from operator import itemgetter
import os
from reportlab.platypus import Table, Paragraph, Spacer
from reportlab.platypus import PageBreak
from enum import Enum, auto
from utilsDatabase import getMovieData
from utilsReport import getReportStyles, getSimpleDocTamplate

class Cols(Enum):
    TSPDT = 0
    TITLE = auto()
    INFO = auto()
    SPINE = auto()
    LOCATION = auto()
    CRITERIONFORMAT = auto()
    CHECKED = auto()

def generate_report(sql_query, reportTitle, pdf_filename):
    data = getMovieData(sql_query)
    styles = getReportStyles()

    # Create a list of formatted cells
    all_rows = []
    all_rows.append(["", Paragraph(f"<b>{reportTitle}</b>", styles['TopTitle']), ""])
    
    for row in data:
        title = f"{row[Cols.TITLE.value]}\n<i>{row[Cols.INFO.value]}</i>\n"

        if row[Cols.LOCATION.value] is not None:
            location = f"{row[Cols.SPINE.value]} {row[Cols.LOCATION.value]}"
        elif row[Cols.CRITERIONFORMAT.value] is not None:
            location =  row[Cols.CRITERIONFORMAT.value]
        else:
            location = ''

        formatted_row = [
            Paragraph(f"{row[Cols.TSPDT.value]}", styles['RightAligned']),
            Paragraph(f"{title}", styles['Small']),
            Paragraph(f"{location}", styles['RightAligned'])
        ]

        all_rows.append(formatted_row)

    pdf_filename = os.path.join(os.path.expanduser(
        '~/Downloads'), pdf_filename)

    # Create the table
    doc = getSimpleDocTamplate(pdf_filename)

    table_width = doc.width - doc.leftMargin - doc.rightMargin
    column_widths = [
        table_width * 0.06,
        table_width * 0.84,
        table_width * 0.10,
    ]
    row_heights = [14] * (len(all_rows) - 1)
    row_heights.insert(0, 30)

    elements = []
    elements.append(Table(all_rows, colWidths=column_widths, rowHeights=row_heights))
    doc.build(elements)

    print(f"PDF report saved to {pdf_filename}")
     
generate_report("select * from tspdt_View limit 100", "They Shoot Pictures Don't They - Not Seen", "tspdt_report.pdf")
generate_report("select * from tspdt2k_view limit 100", "They Shoot Pictures Don't They 2K - Not Seen", "tsptd2k_report.pdf")
generate_report("select * from tspdt_View where checkedLee is null and tspdt is not null and location is not null limit 100", 
                "They Shoot Pictures Don't They - Owned Not Seen", "towatch_report.pdf")