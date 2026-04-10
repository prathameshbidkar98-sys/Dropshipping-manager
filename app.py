from flask import Flask, render_template, request, redirect, session
from database import *

app = Flask(__name__)
app.secret_key = "secret123"

create_table()
create_user_table()

# LOGIN CHECK
def is_logged_in():
    return "user" in session


@app.route("/")
def index():
    if not is_logged_in():
        return redirect("/login")

    orders = get_orders()
    return render_template("index.html", orders=orders)


@app.route("/add", methods=["POST"])
def add():
    if not is_logged_in():
        return redirect("/login")

    product = request.form["product"]
    cost = request.form["cost"]
    selling = request.form["selling"]
    status = request.form["status"]

    add_order(product, cost, selling, status)
    return redirect("/")


@app.route("/delete/<int:id>")
def delete(id):
    if not is_logged_in():
        return redirect("/login")

    delete_order(id)
    return redirect("/")


@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    if not is_logged_in():
        return redirect("/login")

    status = request.form["status"]
    update_status(id, status)
    return redirect("/")


# AUTH SYSTEM
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = login_user(username, password)

        if user:
            session["user"] = username
            return redirect("/")
        else:
            return "Invalid credentials"

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        register_user(username, password)
        return redirect("/login")

    return render_template("signup.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)