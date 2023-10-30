from flask import request, render_template, session, redirect, url_for
from werkzeug.security import check_password_hash

from app import app
from app.database import db
from app.user.models import User


def get_password_from_db(username):
    try:
        query = db.select(User).where(User.username == username)
        result = db.session.execute(query).scalar_one()
    except Exception as e:
        app.logger.error(e)
        return None
    else:
        return result.password


@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        context = {}
        username = request.form.get("username")
        if current_password := get_password_from_db(username):
            password = request.form.get("password")
            if check_password_hash(current_password, password):
                session["username"] = request.form.get("username")
                return redirect(url_for("courses_list"))
            context.update({"error": "Incorrect password"})
        else:
            context.update({"error": "User not found"})
        return render_template("login.html", **context)


@app.route("/logout", methods=["GET"])
def logout():
    del session["username"]
    return redirect(url_for("login_page"))

