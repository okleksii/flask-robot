from flask import request, make_response, render_template, session, redirect, url_for, typing as ft
from flask.views import View, MethodView

from app import app
from app.database import db
from app.course.models import Course, Lesson, LessonUser
from app.course.forms import CourseForm, CourseLessonForm
from app.user.models import User


def get_current_user():
    if username := session.get("username"):
        return db.session.execute(db.select(User).where(User.username == username)).scalar_one()


@app.get("/courses")
def courses_list():
    query = db.select(Course)
    courses = db.session.execute(query).scalars()
    context = {
        "courses": courses,
    }
    return render_template("courses/list.html", **context)


@app.route("/courses/create", methods=["GET", "POST"])
def create_course():
    session["username"] = "admin"
    form = CourseForm()
    if form.validate_on_submit():
        course = Course()
        form.populate_obj(course)
        course.mentor_id = get_current_user().id
        db.session.add(course)
        db.session.commit()
        return redirect(url_for("course_detail", course_id=course.id))
    return render_template("courses/create.html", form=form)


@app.get("/courses/<int:course_id>")
def course_detail(course_id):
    course = db.get_or_404(Course, course_id)
    return render_template("courses/detail.html", course=course)


@app.patch("/courses/<int:course_id>")
def course_update(course_id):
    json = request.json
    return f"<h1>Course {course_id} updated</h1><p>{json}</p>"


@app.route("/courses/<int:course_id>/users")
def course_users(course_id):
    cookies = request.cookies.items()
    context = {
        "cookies": cookies,
        "course_id": course_id,
    }
    resp = make_response(render_template("courses/list_users.html", **context))
    resp.set_cookie("flask", "application")
    return resp


@app.route("/courses/<int:course_id>/lessons")
def course_lessons(course_id):
    course = db.get_or_404(Course, course_id)
    user = get_current_user()
    for lesson in course.lessons:
        if not lesson.registered_users or user not in lesson.registered_users:
            lesson.can_reginster = True
        else:
            lesson.can_register = False
    return render_template("courses/lessons.html", course=course)


@app.route("/courses/<int:course_id>/lessons/create", methods=["GET", "POST"])
def create_course_lesson(course_id):
    form = CourseLessonForm()
    if form.validate_on_submit():
        lesson = Lesson()
        form.populate_obj(lesson)
        lesson.course_id = course_id
        db.session.add(lesson)
        db.session.commit()
        return redirect(url_for("course_lessons", course_id=course_id))
    return render_template("courses/create_lesson.html", form=form)


@app.route("/courses/<int:course_id>/lessons/<int:lesson_id>/register", methods=["GET", "POST"])
def lesson_register(course_id, lesson_id):
    lesson = db.get_or_404(Lesson, lesson_id)
    user = get_current_user()
    if lesson.course_id == course_id and (not lesson.registered_users or user not in lesson.registered_users):
        lesson_user = LessonUser()
        lesson_user.lesson_id = lesson.id
        lesson_user.user_id = user.id
        db.session.add(lesson_user)
        db.session.commit()
    return redirect(url_for("course_lessons", course_id=course_id))


@app.route("/courses/<int:course_id>/lessons/<int:lesson_id>")
def course_lesson(course_id, lesson_id):
    return f"<h1>Lesson {lesson_id} for course {course_id}</h1>"



class BaseListView(View):
    def __init__(self, model):
        self.model = model

    def dispatch_request(self) -> ft.ResponseReturnValue:
        objects = self.model.query.all()
        return render_template("base_list.html", objects=objects)


app.add_url_rule(
    "/base/users",
    view_func=BaseListView.as_view("users-list", User)
)

app.add_url_rule(
    "/base/courses",
    view_func=BaseListView.as_view("courses-list", Course)
)

app.add_url_rule(
    "/base/lessons",
    view_func=BaseListView.as_view("lessons-list", Lesson)
)
