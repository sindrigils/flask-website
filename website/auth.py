from flask import render_template, Blueprint, url_for, redirect, flash
from flask_login import login_required, login_user, logout_user
from website.forms import LoginForm, RegisterForm
from website.models import User
from website import db

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["POST", "GET"])
def login_page():
    """
        This view function handles the login page. It displays a login form to the user,
        and authenticates the user's credentials upon submission of the form.

        Returns:
            --------
            GET: renders the login template.
            POST: redirects the user to the home page if their credentials are valid. Otherwise,
            the user stays on the login page and an error message is flashed.
    """

    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):

            login_user(attempted_user)
            flash(message=f"You successfully logged in as: {attempted_user.username}", category="success")

            return redirect(url_for("views.home_page"))
        
        flash(message="Username and password don't match! Please try again", category="danger")

    return render_template("login.html", form=form)


@auth.route("/register", methods=["POST", "GET"])
def register_page():
    """
        Registers a new user account.

        GET: Display the registration form.
        POST: Process the registration form, validate user input and create a new user account if input is valid.
        Upon successful registration, log the user in and redirect to the home page.

        Returns:
            A rendered HTML template for the registration page with a form to create a new user account.

    """
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
    """
        Logout the current user and redirect to the login page.

        Returns:
            Flask redirect response: Redirects to the login page after logging the user out.

    """ 

    logout_user()
    flash(message="You have been logged out!", category="info")
    return redirect(url_for("auth.login_page"))
