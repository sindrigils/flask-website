from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from dotenv import load_dotenv
import os

load_dotenv()
secret_key = os.getenv("secret_key")
# ts2 = TimeSeries(key=os.getenv("API_KEY"), output_format="pandas")

app = Flask(__name__, template_folder="/Users/sindri/Desktop/stock-website/website/templates")
app.config["SECRET_KEY"] = secret_key
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///market.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

app.app_context().push()

from .auth import auth
app.register_blueprint(auth, url_prefix="/")