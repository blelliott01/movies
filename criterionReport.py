import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import TableStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from databaseUtils import connect
from criterionReportQuery import getQuery

def generate_report(where_clause):
    # Connect to the database
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT 
            title,
            json_extract(omdbData, '$.Director') AS director,
            year,
            criterionSpine,
            shelf,
            rating,
            json_extract(omdbData, '$.Runtime') AS runtime,
            json_extract(omdbData, '$.Country') AS country,
            json_extract(omdbData, '$.Genre') AS genre,
            checkedLee,
            rankTheyShoot
        FROM movies
        WHERE {where_clause}
            AND (CAST(SUBSTR(json_extract(omdbData, '$.Runtime'), 1, LENGTH(json_extract(omdbData, '$.Runtime')) - 4) AS INTEGER) >= 60
                OR json_extract(omdbData, '$.Runtime') IS NULL)
        ORDER BY 
            CASE
                WHEN title LIKE 'A %' THEN SUBSTR(title, 3)
                WHEN title LIKE 'The %' THEN SUBSTR(title, 5)
                ELSE title
            END;
        """)

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

    # Create a list of formatted cells
    formatted_rows = []
    for row in data:
        arrow1 = '>' if row[9] is None else ''
        arrow2 = '>>' if row[10] is not None else ''

        title = f"{row[0]}\n" if row[9] == 'yes' else f"<b>{arrow1}{arrow2} {row[0]}</b>\n" 

        year = f"{row[2]}" if row[2] is not None else 'n/a'
        director = f"{row[1].split(',')[0].strip()}" if row[1] is not None else 'n/a'
        time = f"{row[6]}" if row[6] is not None else 'n/a'

        location = f"{row[3]}.{row[4]}" if row[3] is not None else 'n/a'

        info = f"<i>({year}, {director}, {time})</i>\n" 
        if year is None and director is None and time is None:
            info = ''
        
        ratingMC = f"MC: {row[5]}% " if row[5] is not None else ''
        ratingTS = f"TS: {row[10]} " if row[10] is not None else ''

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

generate_report('criterion is not null')