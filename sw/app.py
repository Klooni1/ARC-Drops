import os
import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session, abort
from werkzeug.security import generate_password_hash, check_password_hash
import config
import itemhandler
import userhandler
import commenthandler
import secrets
import db

def init_db():
    db_path = "database.db"
    if not os.path.exists(db_path):
        con = sqlite3.connect(db_path)
        with open("schema.sql", "r", encoding="utf-8") as f:
            con.executescript(f.read())
        con.close()
init_db()


def get_csrf_token():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(32)
    return session["csrf_token"]

def check_csrf():
    token = session.get("csrf_token")
    form_token = request.form.get("csrf_token")

    if not token or not form_token or token != form_token:
        abort(403)

# --------------------------------------------------------

app = Flask(__name__)
app.secret_key = config.secret_key

@app.context_processor
def inject_csrf_token():
    return {"csrf_token": get_csrf_token()}


@app.route("/")
def index():
    all_items = itemhandler.get_items()
    return render_template("index.html", itemhandler=all_items)

@app.route("/item/<int:item_id>", methods=["GET", "POST"])
def show_item(item_id):
    item = itemhandler.get_item(item_id)
    if request.method == "POST":
        check_csrf()
        if "user_id" not in session:
            return redirect("/login")
        message = request.form.get("message")
        commenthandler.add_comment(item_id, session["user_id"], session["username"], message)
        return redirect(f"/item/{item_id}")
    comments = commenthandler.get_comments_for_item(item_id)
    return render_template("itempage.html", item=item, comments=comments)


@app.route("/find_item")
def find_item():
    query = request.args.get("query", "")
    selected_tag = request.args.get("tag", "")
    if query or selected_tag:
        results = itemhandler.find_items(query, selected_tag)
    else:
        results = []
    return render_template("find_item.html", query=query, selected_tag=selected_tag, results=results)


@app.route("/new_item")
def new_item():
    return render_template("new_item.html")

@app.route("/create_item", methods=["POST"])
def create_item():
    check_csrf()
    enemy_name = request.form["enemy_name"]
    drops = request.form["drops"]
    tag = request.form["tag"]
    user_id = session["user_id"]
    itemhandler.add_item(enemy_name, drops, tag, user_id)
    return redirect("/")


@app.route("/edit_item/<int:item_id>")
def edit_item(item_id):
    item = itemhandler.get_item(item_id)
    return render_template("edit_item.html", item = item)

@app.route("/update_item", methods=["POST"])
def update_item():
    check_csrf()
    item_id = request.form["item_id"]
    enemy_name = request.form["enemy_name"]
    drops = request.form["drops"]
    tag = request.form["tag"]
    itemhandler.update_item(item_id, enemy_name, drops, tag)
    return redirect("/item/" + str(item_id))


@app.route("/delete_item/<int:item_id>", methods=["GET", "POST"])
def delete_item(item_id):
    if request.method == "GET":
        item = itemhandler.get_item(item_id)
        return render_template("delete_item.html", item=item)
    check_csrf()
    if "delete" in request.form:
        itemhandler.delete_item(item_id)
    return redirect("/")


@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    check_csrf()
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    error = None
    success = None
    if password1 != password2:
        error = "Salasanat eivät ole samat"
        return render_template("register.html", error=error)
    password_hash = generate_password_hash(password1)
    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
        success = f"Tunnus '{username}' luotu! Voit nyt kirjautua sisään."
    except sqlite3.IntegrityError:
        error = "Tunnus on jo varattu"
        return render_template("register.html", error=error)
    return render_template("register.html", success=success)


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        get_csrf_token()
        check_csrf()
        results = db.query("SELECT id, password_hash FROM users WHERE username = ?", [username])
        if not results:
            error = "Väärä tunnus tai salasana, yritä uudelleen"
        else:
            user = results[0]
            if check_password_hash(user["password_hash"], password):
                session["user_id"] = user["id"]
                session["username"] = username
                return redirect("/")
            else:
                error = "Väärä tunnus tai salasana"
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    return redirect("/")

@app.route("/users")
def list_users():
    all_users = userhandler.get_users()
    return render_template("users.html", users=all_users)

@app.route("/users/<int:user_id>")
def user_detail(user_id):
    user = userhandler.get_user(user_id)
    if not user:
        return "VIRHE: Käyttäjää ei löytynyt"
    item_count = userhandler.get_user_item_count(user_id)
    added_items = userhandler.get_items_by_user(user_id)
    comment_count = userhandler.get_user_comment_count(user_id)
    return render_template("user_details.html", user=user, item_count=item_count, items=added_items, comment_count=comment_count)

# --------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)