from typing import List

from sqlalchemy import Integer, Text, Boolean
from sqlalchemy.orm import mapped_column, Mapped, relationship, backref
from app.database import db


class User(db.Model):
    id = mapped_column(Integer, primary_key=True)
    first_name = mapped_column(Text)
    last_name = mapped_column(Text)
    username = mapped_column(Text, unique=True)
    password = mapped_column(Text)
    is_mentor = mapped_column(Boolean, default=False)
    mentored_courses: Mapped[List["Course"]] = relationship("Course", backref=backref("mentor"))
    courses: Mapped[List["CourseUser"]] = relationship("CourseUser", backref=backref("user"))
    lessons: Mapped[List["LessonUser"]] = relationship("LessonUser", backref=backref("user"))

