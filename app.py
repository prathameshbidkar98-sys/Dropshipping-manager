from flask import Flask, render_template, request, redirect, session, send_file
import pandas as pd
from database import *

app = Flask(__name__)
app.secret_key = "secret123"

# Create DB table
create_table()


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "1234":
            session["user"] = username
            return redirect("/")
        else:
            return "Invalid Credentials"

    return render_template("login.html")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


# ---------------- DASHBOARD ----------------
@app.route("/")
def index():
    if "user" not in session:
        return redirect("/login")

    orders = get_orders()
    profit = total_profit()

    return render_template("index.html", orders=orders, profit=profit)


# ---------------- ADD ORDER ----------------
@app.route("/add", methods=["POST"])
def add():
    if "user" not in session:
        return redirect("/login")

    date = request.form["date"]
    name = request.form["name"]
    product = request.form["product"]
    cost = request.form["cost"]
    selling = request.form["selling"]
    status = request.form["status"]

    add_order(date, name, product, cost, selling, status)

    return redirect("/")


# ---------------- DELETE ----------------
@app.route("/delete/<int:id>")
def delete(id):
    if "user" not in session:
        return redirect("/login")

    delete_order(id)
    return redirect("/")


# ---------------- UPDATE STATUS ----------------
@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    if "user" not in session:
        return redirect("/login")

    status = request.form["status"]
    update_status(id, status)

    return redirect("/")


# ---------------- EXPORT TO EXCEL ----------------
@app.route("/export")
def export():
    if "user" not in session:
        return redirect("/login")

    conn = connect()
    df = pd.read_sql_query("SELECT * FROM orders", conn)
    conn.close()

    file_name = "orders.xlsx"
    df.to_excel(file_name, index=False)

    return send_file(file_name, as_attachment=True)


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)