from flask import Blueprint
from pythonic.models import Lesson
from flask import render_template, url_for, flash, redirect, request,abort
from pythonic.lessons.forms import NewLessonForm,LessonUpdateForm
from pythonic import  db
from flask_login import (
    login_required,
    current_user,
    login_required,
)

from pythonic.helpers import save_picture
from pythonic.lessons.helpers import get_previous_next_lesson , delete_picture


lessons = Blueprint('lessons',__name__)


@lessons.route("/dashboard/new_lesson", methods=["GET", "POST"])
@login_required
def new_lesson():
    new_lesson_form = NewLessonForm()
    if new_lesson_form.validate_on_submit():
        if new_lesson_form.thumbnail.data:
            picture_file = save_picture(new_lesson_form.thumbnail.data , "static/lesson_thumb")
        course = new_lesson_form.course.data
        lesson_slug = str(new_lesson_form.slug.data).replace(" " , ("-"))
        lesson = Lesson(
            title=new_lesson_form.title.data,
            content=new_lesson_form.content.data,
            slug=lesson_slug,
            author=current_user,
            course_name=course,
            thumbnail = picture_file
        )
        db.session.add(lesson)
        db.session.commit()
        flash("Your lesson has been created!", "success")
        return redirect(url_for("lessons.new_lesson"))

    return render_template(
        "new_lesson.html",
        title="New Lesson",
        new_lesson_form=new_lesson_form,
        active_tab="new_lesson",
    )

@lessons.route("/<string:course>/<string:lesson_slug>")
def lesson(lesson_slug , course): ## داله لعرض اللينك بشكل منظم
    ## لو السلاج بتساوى اللى مديهولو فى الفانكشن
    lesson = Lesson.query.filter_by(slug=lesson_slug).first() 
    if lesson:
        previous_lesson, next_lesson = get_previous_next_lesson(lesson)
    ## لو اللاى دى موجود اللى هو تروو
    lesson_id = lesson.id if lesson else None
    ## من الداتا بيز هات الليسون او ايرور 
    lesson = Lesson.query.get_or_404(lesson_id)
    return render_template("lesson_view.html" ,title = lesson.title , lesson=lesson, previous_lesson=previous_lesson,next_lesson=next_lesson) ## بتساوى اخر قيمه عملتها 

@lessons.route("/dashboard/user_lessons" , methods = ["GET" , "POST"])
@login_required
def user_lessons():
    return render_template(
        "user_lessons.html",
        title="user_lessons",
        active_tab="user_lessons",
    )
    
@lessons.route("/<string:course>/<string:lesson_slug>/update" , methods=["GET","POST"])
def update_lesson(lesson_slug , course): ## داله لعرض اللينك بشكل منظم
    ## لو السلاج بتساوى اللى مديهولو فى الفانكشن
    lesson = Lesson.query.filter_by(slug=lesson_slug).first() 
    if lesson:
        previous_lesson, next_lesson = get_previous_next_lesson(lesson)
    ## لو اللاى دى موجود اللى هو تروو
    lesson_id = lesson.id if lesson else None
    ## من الداتا بيز هات الليسون او ايرور 
    lesson = Lesson.query.get_or_404(lesson_id)
    if lesson.author != current_user:
        abort(403)
    form = LessonUpdateForm()
    if form.validate_on_submit():
        ## POST
        lesson.course_name = form.course.data
        lesson.title = form.title.data
        lesson.slug = str(form.slug.data).replace(" " ,  "-")
        lesson.content = form.content.data
        if form.thumbnail.data:
            delete_picture(lesson.thumbnail , "static/lesson_thumb")
            new_picture = save_picture(form.thumbnail.data , "static/lesson_thumb")
            lesson.thumbnail = new_picture
        db.session.commit()
        flash("Your lesson has been updated!","success")
        return redirect(url_for("lessons.lesson",lesson_slug=lesson.slug , course=lesson.course_name.title))  
    elif request.method == "GET":
        form.course.data = lesson.course_name
        form.title.data = lesson.title
        form.slug.data = lesson.slug
        form.content.data = lesson.content
    return render_template("update_lesson.html" ,title = "Update | " +lesson.title , lesson=lesson, previous_lesson=previous_lesson,next_lesson=next_lesson , form=form) ## بتساوى اخر قيمه عملتها 

@lessons.route("/lesson/<lesson_id>/delete" , methods=["POST"])
def delete_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    if lesson.user_id != current_user.id:
        abort(403)
    db.session.delete(lesson)
    db.session.commit()
    flash("Your lesson has been deleted","success")
    return redirect(url_for("lessons.user_lessons"))

