import json
from urllib.parse import urlparse
from utilsOmdb import getMoviData
from utilsDatabase import connect

# Connect to the database
connection = connect()

cursor = connection.cursor()
cursor.execute("SELECT imdbUrl FROM movies WHERE omdbData IS NULL LIMIT 1000")

imdbUrls = [row[0] for row in cursor.fetchall()]

for imdbUrl in imdbUrls:
    imdbId = urlparse(imdbUrl).path.split('/')[-2]
    omdbData = getMoviData(imdbId)

    if omdbData:
        omdbJson = json.dumps(omdbData)
        cursor.execute("UPDATE movies SET omdbData=? WHERE imdbUrl=?", (omdbJson, imdbUrl))
        connection.commit()
    else:
        print("Failed to retrieve movie data for IMDb ID:", imdbId)

connection.close()
