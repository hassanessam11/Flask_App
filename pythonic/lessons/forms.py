from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms_sqlalchemy.fields import QuerySelectField
from flask_ckeditor import CKEditorField
from wtforms import StringField ,SubmitField
from wtforms.validators import (
    DataRequired,
    Length,
)
from pythonic.models import Course


def choice_query():
    return Course.query

class NewLessonForm(FlaskForm):
    course = QuerySelectField("Course", query_factory=choice_query, get_label="title")
    title = StringField("Lesson Title", validators=[DataRequired(), Length(max=100)])
    slug = StringField(
        "Slug",
        validators=[DataRequired(), Length(max=32)],
        render_kw={
            "placeholder": "Descriptive short version of your title. SEO friendly"
        },
    )
    content = CKEditorField(
        "Lesson Content", validators=[DataRequired()], render_kw={"rows": "5"}
    )
    thumbnail = FileField(
        "Thumbnail", validators=[DataRequired(), FileAllowed(["jpg", "png"])]
    )
    submit = SubmitField("Post")

class LessonUpdateForm(NewLessonForm):
    thumbnail = FileField(
        "Thumbnail", validators=[FileAllowed(["jpg", "png"])]
    )
    submit = SubmitField("Update")