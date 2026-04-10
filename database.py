import sqlite3

def connect():
    return sqlite3.connect("orders.db")

def create_table():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product TEXT,
        cost REAL,
        selling REAL,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()

def add_order(product, cost, selling, status):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO orders (product, cost, selling, status) VALUES (?, ?, ?, ?)",
                   (product, cost, selling, status))

    conn.commit()
    conn.close()

def get_orders():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM orders")
    rows = cursor.fetchall()

    conn.close()
    return rows

def delete_order(id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM orders WHERE id=?", (id,))

    conn.commit()
    conn.close()

def update_status(id, status):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("UPDATE orders SET status=? WHERE id=?", (status, id))

    conn.commit()
    conn.close()


# USER SYSTEM
def create_user_table():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()

def register_user(username, password):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                   (username, password))

    conn.commit()
    conn.close()

def login_user(username, password):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=? AND password=?",
                   (username, password))

    user = cursor.fetchone()
    conn.close()

    return user