import datetime
from typing import List

from sqlalchemy import Integer, Text, ForeignKey, Date
from sqlalchemy.orm import mapped_column, relationship, Mapped, backref
from app.database import db


class Course(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    mentor_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    begin_at: Mapped[datetime.date] = mapped_column(Date)
    end_at: Mapped[datetime.date] = mapped_column(Date)
    users: Mapped[List["CourseUser"]] = relationship("CourseUser", backref=backref("course"))
    lessons: Mapped[List["Lesson"]] = relationship("Lesson", backref=backref("course"))


class CourseUser(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    course_id: Mapped[int] = mapped_column(Integer, ForeignKey("course.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    mark: Mapped[int] = mapped_column(Integer)
    begin_at: Mapped[datetime.date] = mapped_column(Date)
    end_at: Mapped[datetime.date] = mapped_column(Date)


class Lesson(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    course_id: Mapped[int] = mapped_column(Integer, ForeignKey("course.id"), nullable=False)
    begin_at: Mapped[datetime.date] = mapped_column(Date)
    registered_users: Mapped[List["LessonUser"]] = relationship("LessonUser", backref=backref("lesson"))


class LessonUser(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lesson_id: Mapped[int] = mapped_column(Integer, ForeignKey("lesson.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    hometask: Mapped[str] = mapped_column(Text, nullable=True)
    mark: Mapped[int] = mapped_column(Integer, nullable=True)
