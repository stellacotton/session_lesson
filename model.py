import sqlite3

def connect_to_db():
    global CONN, DB
    CONN = sqlite3.connect("thewall.db")
    DB = CONN.cursor()


def authenticate(username, password):
    connect_to_db()
    query = """SELECT id, username, password FROM users WHERE username = ? and password = ?"""
    DB.execute(query, (username, password))
    row = DB.fetchone()
    if row:
        user_id = row[0]
        return user_id

    else:
        return None

def get_user_by_name(username):
    connect_to_db()
    query = """SELECT id FROM users WHERE username = ?"""
    DB.execute(query, (username,))
    user_id = DB.fetchone()
    if user_id:
        return user_id[0]
    else: 
        return "Nope"

def get_wall_posts(user_id):
    connect_to_db()
    query = """SELECT username, created_at, content FROM wall_posts LEFT JOIN users ON users.id = wall_posts.author_id WHERE owner_id = ?"""
    DB.execute(query, (user_id,))
    rows = DB.fetchall()
    return rows


def post_to_wall(user_id, author_id, datetime, content):
    connect_to_db()
    query = """INSERT into wall_posts(owner_id, author_id, created_at, content) VALUES (?,?,?,?)"""
    DB.execute(query, (user_id, author_id, datetime, content))
    CONN.commit()

def register_new_user(username, password):
    connect_to_db()
    query = """INSERT into users(username, password) VALUES (?,?)"""
    DB.execute(query, (username, password))
    CONN.commit()