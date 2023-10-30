from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms.validators import DataRequired


class CourseForm(FlaskForm):
    name = StringField(label="Name", validators=[DataRequired()])
    description = StringField(label="Description", validators=[DataRequired()])
    begin_at = DateField(label="Begin at", validators=[DataRequired()])
    end_at = DateField(label="End at", validators=[DataRequired()])


class CourseLessonForm(FlaskForm):
    name = StringField(label="Name", validators=[DataRequired()])
    description = StringField(label="Description", validators=[DataRequired()])
    begin_at = DateField(label="Begin at", validators=[DataRequired()])
