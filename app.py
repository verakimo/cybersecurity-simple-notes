import sqlite3
import secrets

from flask import Flask, render_template, request, redirect, url_for, session, abort
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = "dev-secret-key"

DATABASE = "notes.db"


def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db


@app.route("/")
def index():
    db = get_db()

    notes = db.execute("SELECT * FROM notes ORDER BY id DESC").fetchall()

    db.close()

    # FLAW 5: CSRF
    # The application does not generate a CSRF token for the user's session.

    # FIX:
    # if "user_id" in session and "csrf_token" not in session:
    #     session["csrf_token"] = secrets.token_hex(32)

    return render_template("index.html", notes=notes)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # FLAW 2: A3:2017 Sensitive Data Exposure - Plaintext password storage
        db = get_db()
        db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))

        # FIX:
        # password_hash = generate_password_hash(password)
        # db = get_db()
        # db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password_hash))

        db.commit()
        db.close()

        return redirect(url_for("index"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()

        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        db.close()

        # FLAW 2: A3:2017 Sensitive Data Exposure - Plaintext password comparison
        if user is not None and user["password"] == password:
            session["user_id"] = user["id"]
            session["username"] = user["username"]

            return redirect(url_for("index"))

        # FIX:
        # if user is not None and check_password_hash(user["password"], password):
        #     session["user_id"] = user["id"]
        #     session["username"] = user["username"]
        #
        #     return redirect(url_for("index"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/notes/new", methods=["GET", "POST"])
def create_note():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        db = get_db()

        db.execute("INSERT INTO notes (title, content, owner_id) VALUES (?, ?, ?)",(title, content, session["user_id"]))

        db.commit()
        db.close()

        return redirect(url_for("index"))

    return render_template("new_note.html")


@app.route("/notes/<int:note_id>/edit", methods=["GET", "POST"])
def edit_note(note_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    db = get_db()

    note = db.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()

    if note is None:
        db.close()
        abort(404)

    # FLAW 3: A5:2017 Broken Access Control
    # The application does not check whether the current user owns the note.

    # FIX:
    # if note["owner_id"] != session["user_id"]:
    #     db.close()
    #     abort(403)

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        db.execute("UPDATE notes SET title = ?, content = ? WHERE id = ?", (title, content, note_id))

        db.commit()
        db.close()

        return redirect(url_for("index"))

    db.close()

    return render_template("edit_note.html", note=note)


@app.route("/notes/<int:note_id>/delete", methods=["POST"])
def delete_note(note_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    # FLAW 5: CSRF
    # The application does not check a CSRF token before deleting a note.

    # FIX:
    # if request.form.get("csrf_token") != session.get("csrf_token"):
    #     abort(403)

    db = get_db()

    note = db.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()

    if note is None:
        db.close()
        abort(404)

    if note["owner_id"] != session["user_id"]:
        db.close()
        abort(403)

    db.execute("DELETE FROM notes WHERE id = ?", (note_id,))

    db.commit()
    db.close()

    return redirect(url_for("index"))


@app.route("/search")
def search():
    search_term = request.args.get("q", "")

    db = get_db()

    # FLAW 1: A1:2017 Injection - SQL Injection
    query = ("SELECT * FROM notes WHERE title LIKE '%" + search_term + "%'")
    notes = db.execute(query).fetchall()

    # Fix:
    # notes = db.execute("SELECT * FROM notes WHERE title LIKE ?", ("%" + search_term + "%",)).fetchall()

    db.close()

    return render_template("search.html", notes=notes, search_term=search_term)
