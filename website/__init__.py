from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from dotenv import load_dotenv
import os



load_dotenv()
secret_key = os.getenv("secret_key")

app = Flask(__name__, template_folder="/Users/sindri/Desktop/flask-website/website/templates")
app.config["SECRET_KEY"] = secret_key
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///market.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = "auth.login_page"
login_manager.login_message_category = "info"


app.app_context().push()

from .auth import auth
app.register_blueprint(auth, url_prefix="/")

from .views import views
app.register_blueprint(views, url_prefix="/")


from website.models import User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))