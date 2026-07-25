import sqlite3

conn = sqlite3.connect("backend/movies.db")
cursor = conn.cursor()
cursor.execute(
    "DELETE FROM movies where id >0 " 
)
conn.commit()
conn.close()