import os
import csv
from databaseUtils import connect
from criterionReportQuery import getQuery

# Connect to the database
conn = connect()
cursor = conn.cursor()
cursor.execute(getQuery())
data = cursor.fetchall()

# Close the database connection
conn.close()

downloads_folder = os.path.expanduser('~/Downloads')
csv_filename = os.path.join(downloads_folder, 'movie_report.csv')

# Export data to CSV
with open(csv_filename, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['title', 'spine'])
    csv_writer.writerows(data)

print(f"CSV data exported to {csv_filename}")
