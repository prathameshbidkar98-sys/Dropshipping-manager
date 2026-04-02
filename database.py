import sqlite3

def connect():
    return sqlite3.connect("orders.db")


def create_table():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        name TEXT,
        product TEXT,
        cost REAL,
        selling REAL,
        profit REAL,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()


def add_order(date, name, product, cost, selling, status):
    conn = connect()
    cursor = conn.cursor()

    profit = float(selling) - float(cost)

    cursor.execute("""
    INSERT INTO orders (date, name, product, cost, selling, profit, status)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (date, name, product, cost, selling, profit, status))

    conn.commit()
    conn.close()


def get_orders():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM orders ORDER BY id DESC")
    data = cursor.fetchall()

    conn.close()
    return data


def delete_order(order_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))

    conn.commit()
    conn.close()


def update_status(order_id, status):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("UPDATE orders SET status = ? WHERE id = ?", (status, order_id))

    conn.commit()
    conn.close()


def total_profit():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(profit) FROM orders")
    result = cursor.fetchone()[0]

    conn.close()
    return result if result else 0