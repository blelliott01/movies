import os
import requests
from urllib.parse import urlparse
from utilsDatabase import connect

# Connect to the database
connection = connect()

cursor = connection.cursor()
cursor.execute("""
    SELECT imdbUrl, json_extract(omdbData, '$.Poster')
    FROM movies
    WHERE (tspdt IS NOT NULL OR owned IS NOT NULL)
    AND omdbData IS NOT NULL
""")
rows = cursor.fetchall()

# Create the 'images' subfolder if it doesn't exist
if not os.path.exists('images'):
    os.makedirs('images')

for row in rows:
    imdbUrl = row[0]
    poster_url = row[1]

    imdbId = urlparse(imdbUrl).path.split('/')[-2]
    image_filename = f'images/{imdbId}.jpg'

    if os.path.exists(image_filename):
        print(f"Image for IMDb ID {imdbId} already exists as {image_filename}. Skipping...")
        continue

    if poster_url and poster_url != 'N/A':
        response = requests.get(poster_url)
        if response.status_code == 200:
            with open(image_filename, 'wb') as f:
                f.write(response.content)
            print(f"Image for IMDb ID {imdbId} saved as {image_filename}")
        else:
            print(f"Failed to retrieve image for IMDb ID {imdbId}")
    else:
        print(f"No valid poster URL available for IMDb ID {imdbId}")

connection.close()
