from website import app
from flask import render_template, Blueprint, request, url_for, redirect, flash
from flask_login import current_user, login_required, login_user, logout_user
from website.forms import LoginForm, RegisterForm
from website.models import User, Stock
from website import db

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["POST", "GET"])
def login_page():

    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):

            login_user(attempted_user)
            flash(message=f"You successfully logged in as: {attempted_user.username}", category="success")

            return redirect(url_for("views.home_page"))
        
        else:
            flash(message="Username and password don't match! Please try again", category="danger")

    return render_template("login.html", form=form)


@auth.route("/register", methods=["POST", "GET"])
def register_page():

    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(
            username=form.username.data,
            phone_number=form.phone_number.data,
            email_address=form.email_address.data,
            password=form.password1.data)
        
        db.session.add(user_to_create)
        db.session.commit()
        flash(message=f"Account created successfully, welcome {user_to_create.username}", category="success")
        login_user(user_to_create)
        return redirect(url_for("views.home_page"))
    
    if form.errors != {}:
        for error_msg in form.errors.values():
            flash(message=f"There was an error with creating the user: {error_msg}", category="danger")

        

    return render_template("register.html", form=form)


@auth.route("/logout")
@login_required
def logout_page():

    logout_user()
    flash(message="You have been logged out!", category="info")
    return redirect(url_for("auth.login_page"))