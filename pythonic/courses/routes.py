from flask import Blueprint
from pythonic.models import Lesson, Course
from flask import render_template, url_for, flash, redirect, request
from pythonic.courses.forms import NewCourseForm
from pythonic import db
from flask_login import (
    login_required,
    login_required,
)

from pythonic.helpers import save_picture


courses_bp = Blueprint('courses_bp' , __name__)



@courses_bp.route("/dashboard/new_course" , methods=["GET" , "POST"])
@login_required
def new_course():
    new_course_form = NewCourseForm()
    if new_course_form.validate_on_submit():
        if new_course_form.icon.data:
            picture_file = save_picture(new_course_form.icon.data , "static/course_icon" , output_size=(150,150))
        course_title = str(new_course_form.title.data).replace(" " , ("-"))
        course = Course(
            title = course_title,
            description = new_course_form.description.data,
            icon = picture_file
        )
        db.session.add(course)
        db.session.commit()
        flash("Your course has been created!", "success")
        return redirect(url_for("courses_bp.new_course"))

    return render_template(
        "new_course.html",
        title="New course",
        new_course_form=new_course_form,
        active_tab="new_course",
    )


@courses_bp.route("/<course_title>")
def course(course_title):
    course = Course.query.filter_by(title=course_title).first()
    course_id  = course.id if course else None
    course = Course.query.get_or_404(course_id)
    page = request.args.get('page',1,type=int)
    lessons = Lesson.query.filter_by(course_id=course_id).paginate(page=page,per_page=6)
    return render_template("course.html" , title = course.title , course=course ,lessons=lessons)

@courses_bp.route("/Courses")
def courses():
    page = request.args.get('page',1,type=int)
    courses= Course.query.paginate(page=page,per_page=6)
    return render_template("courses.html" , title ="Courses" , courses=courses)

