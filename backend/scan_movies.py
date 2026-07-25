import os
from flask import Flask
from database import get_movies
import sqlite3

files=os.listdir(r"C:\Users\mmari\Desktop\Netflix 2.0\movies")
existent_movies = get_movies()

def movie_exists_in_db(name, existing_movies):
    for movie in existent_movies:
        if movie['name'] == name:
            return True
    return False

for file in files:
    if file.endswith(".mp4"):
        movie_name = file[:-4]  
        if not movie_exists_in_db(movie_name, existent_movies):
            conn = sqlite3.connect("backend/movies.db")
            cursor = conn.cursor()
            try: 
                cursor.execute(
                    "INSERT INTO movies (name, filename, genre, collection, watch_count, kid_appropriate) VALUES (?, ?, ?, ?, ?, ?)",
                    (movie_name, f"movies/{file}", "Unknown", "Unknown", 0, 0))
            except:
                print(f"Skipped duplicate: {movie_name}")
            conn.commit()
            conn.close()
