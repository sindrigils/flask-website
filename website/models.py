from flask_login import UserMixin
from website import db, bcrypt
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    """
    Represents a user of the application.

    Attributes:
        id (int): The unique identifier of the user.
        username (str): The username of the user (must be unique).
        phone_number (str): The phone number of the user (must be unique).
        email_address (str): The email address of the user (must be unique).
        password_hash (str): The hashed password of the user.
        stocks (List[Stock]): A list of stocks owned by the user.

    Methods:
        password: The password property of the user.
        password.setter: The setter method for the password property.
        check_password_correction: Checks if the provided password matches the user's hashed password.
        check_if_user_own_this_stock: Checks if the user owns a specific stock.
        can_sell: Checks if the user can sell a specific number of shares of a stock they own.

    """
        
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    phone_number = db.Column(db.String(), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(), nullable=False)
    accounts = db.relationship("Account", backref="user", lazy=True)
    stocks = db.relationship("Stock", backref="user_ref", lazy=True)


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

    def check_if_user_own_this_stock(self, stock_ticker: str) -> bool:
        for stock in self.stocks:
            if stock.ticker == stock_ticker:
                return True
        return False

    def can_sell(self, stock_ticker: str, shares: float) -> bool:
        stock = Stock.query.filter_by(user_id=self.id, ticker=stock_ticker).first()
        return stock.shares >= shares


    def can_buy(self, total_cost):
        account = Account.query.filter_by(user_id=self.id).first()

        return account.balance >= total_cost
        
        

class Stock(db.Model):
    """
    A class representing a stock in the database.

    Attributes:
        id (int): The unique ID of the stock in the database.
        ticker (str): The ticker symbol of the stock.
        average_price (float): The average price of the stock for the user.
        shares (float): The number of shares the user owns for the stock.
        date (datetime): The date and time the stock was added to the database.
        user_id (int): The ID of the user who owns the stock.
    """

    id = db.Column(db.Integer(), primary_key=True)
    ticker = db.Column(db.String(length=5), nullable=False)
    average_price = db.Column(db.Float(), nullable=False)
    shares = db.Column(db.Float(), nullable=False)
    cost_basis = db.Column(db.Float(), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self) -> str:
        return f"Stock: {self.ticker} at {self.average_price}$"
    

class Account(db.Model):
    """
    A class representing a user's account in the database.

    Attributes:
        id (int): The unique ID of the account in the database.
        account_owner (int): The ID of the user who owns the account.
        balance (float): The current balance of the account.

    """
    
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    balance = db.Column(db.Float(), nullable=False, default=1_000_000)
    user_ref = db.relationship("User", backref=db.backref("user_accounts", lazy=True), overlaps="accounts,user")



    @property
    def prettier_balance(self):
        # balance_int = int(self.balance * 100)
        # balance_str = f'{balance_int:09d}'
        # groups = [balance_str[-i-3:-i] for i in range(0, len(balance_str), 3)]
        # groups.reverse()
        # return f"{','.join(groups)}{balance_str[-2:]}$"
        return self.balance


    def deposit(self, amount):
        self.balance += amount


    def withdraw(self, amount):
        if amount > self.balance:
            return "Not enough money on account!"
        self.balance -= amount

