import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def get_movies():
    conn = sqlite3.connect("backend/movies.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies")
    rows = cursor.fetchall()
    conn.close()

    movies = []
    for row in rows:
        movies.append({
            "id": row[0],
            "name": row[1],
            "filename": row[2],
            "genre": row[3],
            "collection": row[4],
            "watch_count": row[5],
            "kid_appropriate": row[6]
        })
    return movies

def get_user(user_client):
    conn = sqlite3.connect("backend/users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE name = ?", (user_client,))
    row = cursor.fetchone()
    conn.close()
    return row

def create_user(username, plain_password, role):
    hashed_password = generate_password_hash(plain_password)
    conn = sqlite3.connect("backend/users.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, password, Role) VALUES (?, ?, ?)", (username, hashed_password, role))
    conn.commit()
    conn.close()