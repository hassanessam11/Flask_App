
from pythonic.models import User, Lesson
from flask import render_template, url_for, flash, redirect, request
from flask import Blueprint
from pythonic.users.forms import  RegistrationForm, LoginForm, UpdateProfileForm
from pythonic import bcrypt, db
from flask_login import (
    login_required,
    login_user,
    current_user,
    logout_user,
    login_required,
)
from pythonic.helpers import save_picture



users = Blueprint('users',__name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated: ## لو هو مسجل اصلا 
        return redirect(url_for("main.home"))
    form = RegistrationForm()
    if form.validate_on_submit(): ## لما يدوس على الزرار

        ## يشفر الباسورد
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )

        ## يضيف فى الداتا بيز
        user = User(
            fname=form.fname.data,
            lname=form.lname.data,
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            is_teacher=form.is_teacher.data
        )
        db.session.add(user)
        db.session.commit()
        flash(f"Account created successfully for {form.username.data}", "success")
        return redirect(url_for("users.login")) ## يحولنى على صفحه اللوجن
    return render_template("register.html", title="Register", form=form) ## عشان لو دوست على اللينك يحولنى على الصفحه


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated: ## لو مسجل ودينى على الهوم
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        ## يدور على يوزر بنفس الايميل 
        user = User.query.filter_by(email=form.email.data).first() 
        ## لو الايميل و الباسورد زى بعض 
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            ## يعمل لوجن
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            flash("You have been logged in!", "success")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash("Login Unsuccessful. Please check credentials", "danger")
    return render_template("login.html", title="Login", form=form)


@users.route("/logout")
def logout():
    ## يعمل لوج اوت و يرجع للهوم
    logout_user()
    return redirect(url_for("main.home"))


@users.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    return render_template("dashboard.html", title="Dashboard", active_tab=None)


@users.route("/dashboard/profile", methods=["GET", "POST"])
@login_required
def profile():
    profile_form = UpdateProfileForm()
    if profile_form.validate_on_submit(): ## لما يعمل تحديث
        if profile_form.picture.data:
            picture_file = save_picture(profile_form.picture.data , "static/user_pics" , output_size=(150,150))
            current_user.image_file = picture_file
        
        ## بساوى اللى فى الداتا بيز ب الجديد اللى هو دخله
        current_user.username = profile_form.username.data
        current_user.email = profile_form.email.data
        current_user.bio = profile_form.bio.data
        db.session.commit()
        flash("Your profile has been updated", "success")
        return redirect(url_for("users.profile"))
    elif request.method == "GET":
        ## لو داخل منغير تعديل بساوى اللى قدامه ب اللى فى الداتا بيز
        profile_form.username.data = current_user.username
        profile_form.email.data = current_user.email
        profile_form.bio.data = current_user.bio
    image_file = url_for("static", filename=f"user_pics/{current_user.image_file}")
    return render_template(
        "profile.html",
        title="Profile",
        profile_form=profile_form,
        image_file=image_file,
        active_tab="profile",
    )
@users.route("/author/<string:username>", methods=["GET"])
def author(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    lessons = (
        Lesson.query.filter_by(author=user)
        .order_by(Lesson.date_posted.desc())
        .paginate(page=page, per_page=6)
    )
    return render_template('author.html', lessons=lessons, user=user)