from flask_login import UserMixin
from website import db, bcrypt
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    phone_number = db.Column(db.String(), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(), nullable=False)
    stocks = db.relationship("Stock", backref="owned_user", lazy=True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, text_password: str):
        self.password_hash = bcrypt.generate_password_hash(password=text_password).decode("utf-8")
    
    def check_password_correction(self, attempted_password: str) -> bool:
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    
    def __repr__(self) -> str:
        return f"User {self.username}"
    


class Stock(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    ticker = db.Column(db.String(length=5), nullable=False)
    bought_price = db.Column(db.Float(), nullable=False)
    shares = db.Column(db.Float(), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self) -> str:
        return f"Stock: {self.ticker} at {self.bought_price}$"