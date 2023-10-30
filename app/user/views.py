import random
import string

from flask import render_template, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from app import app
from app.database import db
from app.user.forms import UserRegistrationForm
from app.user.models import User


@app.route("/users")
def get_users():
    query = db.select(User)
    users = db.session.execute(query).scalars()
    return render_template("users/list.html", users=users)


@app.route("/users/<int:user_id>")
def user_detail(user_id):
    return render_template("users/detail.html", user_id=user_id)


@app.route("/registration", methods=["GET", "POST"])
def create_user():
    form = UserRegistrationForm()
    if form.validate_on_submit() and form.password.data == form.repeat_password.data:
        user = User()
        form.populate_obj(user)
        user.password = generate_password_hash(user.password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("courses_list"))
    return render_template("users/registration.html", form=form)
