import os
import sqlite3

def connect():

    db_filename = 'movies/movie.db'

    parent_folder = os.path.abspath(
        os.path.join(os.path.dirname(__file__), 
        os.pardir)
    )
    
    db_path = os.path.join(
        parent_folder, 
        db_filename
    )

    return sqlite3.connect(db_path)