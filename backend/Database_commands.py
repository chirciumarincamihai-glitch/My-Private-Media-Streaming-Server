import sqlite3
conn = sqlite3.connect("movies.db")
cursor = conn.cursor()
conn.commit()
cursor.execute('''
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    filename TEXT,
    genre TEXT,
    collection TEXT,
    watch_count INTEGER,
    kid_appropriate INTEGER,
    CONSTRAINT name_UNIQUE UNIQUE (name)
)''')
conn.commit()
cursor.execute(
    "INSERT INTO movies (name, filename, genre, collection, watch_count, kid_appropriate) VALUES (?, ?, ?, ?, ?, ?)",
    ("Scooby-Doo! and Kiss Rock and Roll Mystery", "Scooby-Doo! and Kiss Rock and Roll Mystery.mp4", "cartoon", "scooby doo", 0, 1)
)
conn.commit()
conn.close()
