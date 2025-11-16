import os
import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import config
import itemhandler
import db

def init_db():
    db_path = "database.db"
    if not os.path.exists(db_path):
        con = sqlite3.connect(db_path)
        with open("schema.sql", "r", encoding="utf-8") as f:
            con.executescript(f.read())
        con.close()
init_db()

# --------------------------------------------------------

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    all_items = itemhandler.get_items()
    return render_template("index.html", itemhandler=all_items)

@app.route("/item/<int:item_id>")
def show_item(item_id):
    item = itemhandler.get_item(item_id)
    return render_template("itempage.html", item = item)

@app.route("/find_item")
def find_item():
    query = request.args.get("query")
    if query:
        results = itemhandler.find_items(query)
    else:
        query = ""
        results = []
    return render_template("find_item.html", query=query, results=results)

@app.route("/new_item")
def new_item():
    return render_template("new_item.html")

@app.route("/create_item", methods=["POST"])
def create_item():
    enemy_name = request.form["enemy_name"]
    drops = request.form["drops"]
    user_id = session["user_id"]
    itemhandler.add_item(enemy_name, drops, user_id)
    return redirect("/")

@app.route("/edit_item/<int:item_id>")
def edit_item(item_id):
    item = itemhandler.get_item(item_id)
    return render_template("edit_item.html", item = item)

@app.route("/update_item", methods=["POST"])
def update_item():
    item_id = request.form["item_id"]
    enemy_name = request.form["enemy_name"]
    drops = request.form["drops"]
    itemhandler.update_item(item_id, enemy_name, drops)
    return redirect("/item/" + str(item_id))

@app.route("/delete_item/<int:item_id>", methods=["GET", "POST"])
def delete_item(item_id):
    if request.method == "GET":
       item = itemhandler.get_item(item_id)
       return render_template("delete_item.html", item = item)
    if request.method == "POST":
        if "delete" in request.form:
            itemhandler.delete_item(item_id)
            return redirect("/")
        else:
            return redirect("/")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
       username = request.form["username"]
       password = request.form["password"]
    
       sql = "SELECT id, password_hash FROM users WHERE username = ?"
       result = db.query(sql, [username])[0]
       user_id = result["id"]
       password_hash = result["password_hash"]

       if check_password_hash(password_hash, password):
           session["user_id"] = user_id
           session["username"] = username
           return redirect("/")
       else:
           return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)