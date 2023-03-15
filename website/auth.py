from website import app
from flask import render_template, Blueprint, request, url_for, redirect, flash
from website.forms import LoginForm, RegisterForm
from website.models import User, Stock
from website import db

auth = Blueprint("auth", __name__)

@auth.route("/")
def home_page():
    return render_template("home.html")


@auth.route("/login", methods=["POST", "GET"])
def login_page():
    
    return render_template("login.html")


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
        
        return redirect(url_for("auth.home_page"))

    return render_template("register.html", form=form)