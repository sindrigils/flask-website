from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from website.models import User

class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        
        if user:
            raise ValidationError(message=f"Username already exists, please try a different username!")
    

    def validate_email_address(self, email_address_to_check):
        email = User.query.filter_by(email_address=email_address_to_check.data).first()

        if email:
            raise ValidationError(message=f"Email address already exists, please try a different email address!")
    
    def validate_phone_number(self, phone_number_to_check):
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
    username = StringField(label="Username: ", validators=[DataRequired()])
    password = PasswordField(label="Password: ", validators=[DataRequired()])
    submit = SubmitField(label="Sign in")
