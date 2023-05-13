from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from website.models import User
from string import punctuation

class RegisterForm(FlaskForm):
    """
    A class representing a registration form for new users.

    Attributes:
        username (StringField): The username of the new user.
        phone_number (StringField): The phone number of the new user.
        email_address (StringField): The email address of the new user.
        password1 (PasswordField): The password entered by the new user.
        password2 (PasswordField): The confirmation password entered by the new user.
        submit (SubmitField): The button to submit the registration form.

    Methods:
        validate_username: Validates the entered username against the database and username not allowed to have punctutaions.
        validate_email_address: Validates the entered email address against the database.
        validate_phone_number: Validates the entered phone number against the database.
    """

    def validate_username(self, username_to_check: str):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError(message=f"Username already exists, please try a different username!")
        
        if any(char in punctuation for char in username_to_check.data):
            raise ValidationError(message=f"Username should not contain any punctuations!")
    

    def validate_email_address(self, email_address_to_check: str):
        email = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email:
            raise ValidationError(message=f"Email address already exists, please try a different email address!")
    
    def validate_phone_number(self, phone_number_to_check: str):
        phone = User.query.filter_by(phone_number=phone_number_to_check.data).first()
        if phone:
            raise ValidationError(message="Phone number already exists, please try a different phone number!")
        

    username = StringField(label="Username: ", validators=[Length(min=2, max=30), DataRequired()])
    phone_number = StringField(label="Phone number: ", validators=[DataRequired()])
    email_address = StringField(label="Emal: ", validators=[Email(), DataRequired()])
    password1 = PasswordField(label="Password: ", validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label="Confirm Password: ", validators=[EqualTo("password1"), DataRequired()])
    submit = SubmitField(label="Create Account")


class LoginForm(FlaskForm):
    """
    A class representing a login form for existing users.

    Attributes:
        username (StringField): The username of the user.
        password (PasswordField): The password of the user.
        submit (SubmitField): The button to submit the login form.

    Methods:
        validate_user_name: Validates that the username has no puntuations.
    """

    def validate_username(self, username_to_check: str):
        if any(char in punctuation for char in username_to_check.data):
            raise ValidationError(message=f"Username should not contain any punctuations!")
    

    username = StringField(label="Username: ", validators=[DataRequired()])
    password = PasswordField(label="Password: ", validators=[DataRequired()])
    submit = SubmitField(label="Sign in")


class StockTickerForm(FlaskForm):
    """
    A class representing a form to get stock ticker information.

    Attributes:
        stock_ticker (StringField): The stock ticker to get information for.
        submit (SubmitField): The button to submit the form.
    """

    stock_ticker = StringField(label="Stock ticker: ", validators=[Length(min=2, max=5), DataRequired()])
    submit = SubmitField(label="Get stock ticker")


class PurchaseStockForm(FlaskForm):
    """
    A class representing a form to purchase a stock.

    Attributes:
        shares (FloatField): The number of shares to purchase.
        submit (SubmitField): The button to submit the form.
    """

    shares = FloatField(label="Shares: ", validators=[DataRequired()])
    submit = SubmitField(label="Purchase stock!")


class SellStockForm(FlaskForm):
    """
    A class representing a form to sell a stock.

    Attributes:
        stock_ticker (StringField): The stock ticker to sell.
        shares (FloatField): The number of shares to sell.
        submit (SubmitField): The button to submit the form.
    """

    stock_ticker = StringField(label="Stock ticker: ", validators=[DataRequired()])
    shares = FloatField(label="Shares: ", validators=[DataRequired()])
    submit = SubmitField(label="Sell stock!")
