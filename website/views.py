from flask import render_template, redirect, url_for, Blueprint, flash
from flask_login import login_required, current_user
from website import db
from website.models import Stock, Account
from website.forms import StockTickerForm, PurchaseStockForm, SellStockForm, AccountForm
from website.stock.stock_models import get_stock_price_by_ticker, plot_a_graph
from copy import deepcopy

views = Blueprint("views", __name__)


@views.route("/")
def home_page():
    return render_template("home.html")


@views.route("/stock_ticker", methods=["POST", "GET"])
@login_required
def stock_ticker_page():
    """
    A function that handles the stock ticker page.

    Methods:
        GET: Renders the stock ticker page.
        POST: Retrieves the stock price for the given stock ticker and displays it on the page.

    Returns:
        render_template: A Flask function that renders a template containing the stock ticker form and the retrieved stock price.
    """

    form = StockTickerForm()
    
    if form.validate_on_submit():
        stock_ticker = form.stock_ticker.data
        stock_ticker = stock_ticker.upper()
        stock_price = get_stock_price_by_ticker(stock_ticker)
    
        return render_template("get_stock.html", form=form, stock_ticker=stock_ticker, stock_price=stock_price)
    
    return render_template("get_stock.html", form=form)


@views.route("/buy_stock<stock_ticker>/<stock_price>", methods=["POST", "GET"])
@login_required
def buy_stock_page(stock_ticker, stock_price):
    """
    This view function allows the user to buy stocks. It retrieves the stock ticker and price passed through the URL.
    It then instantiates a form to enter the number of shares to purchase. If the form is submitted, it first checks
    if the user already owns the stock, and if so, it adds the new shares to the existing shares and updates the average price.
    If not, it adds the new stock to the database. It then flashes a success message and redirects the user to the stock ticker page.
    If the form is not submitted, it renders the "buy_stock.html" template with the form, stock ticker, stock price and the filename
    of the plot generated for that stock ticker. 

    :param stock_ticker: A string representing the stock ticker to buy.
    :param stock_price: A string representing the current price of the stock.
    :return: A rendered HTML template that displays the purchase form, stock ticker, stock price and the filename
    of the plot generated for that stock ticker.
    """


    form = PurchaseStockForm()
    filename = plot_a_graph(stock_ticker)

    if form.validate_on_submit():

        if not current_user.can_buy(total_cost=float(stock_price)*float(form.shares.data)):
            flash(message=f"You dont have enough money to buy this amount of shares!", category="danger")
            return redirect(url_for("views.profile_page"))
        
        buy_stock = Stock(
            ticker=stock_ticker,
            average_price=stock_price,
            shares=form.shares.data,
            cost_basis=float(form.shares.data) * float(stock_price),
            user_id=current_user.id)
        
        owned_stock = Stock.query.filter_by(user_id=current_user.id, ticker=stock_ticker).first() # check if the user already owns this stock if so than add up his shares
        if owned_stock:

            # update the stock
            old_total_shares = owned_stock.shares
            new_total_shares = old_total_shares + form.shares.data

            old_cost_basis = owned_stock.cost_basis
            new_cost_basis = old_cost_basis + (form.shares.data * float(stock_price))

            new_average_price = new_cost_basis / new_total_shares

            owned_stock.shares = new_total_shares
            owned_stock.average_price = new_average_price
            owned_stock.cost_basis = new_cost_basis

        else:
            db.session.add(buy_stock)

        # update the account
        account = Account.query.filter_by(user_id=current_user.id).first()
        account.balance -= float(form.shares.data) * float(stock_price) 

        db.session.commit()

        flash(message=f"You have bought the stock successfully!", category="success")
        return redirect(url_for("views.profile_page"))

    return render_template("buy_stock.html", form=form, stock_ticker=stock_ticker, stock_price=stock_price, filename=filename)



@views.route("/profile", methods=["POST", "GET"])
@login_required
def profile_page():
    """
    Displays the profile page for the logged-in user. If the user submits the account creation form on this page, a new bank account is created for them and added to the database. 

    Returns:
        render_template: Flask function that renders the profile.html template with the owned_stocks and account information.
    """

    form = AccountForm()

    if form.validate_on_submit():
        account_created = Account(user_id=current_user.id)

        db.session.add(account_created)
        db.session.commit()


    owned_stocks = Stock.query.filter_by(user_id=current_user.id)
    has_account = Account.query.filter_by(user_id=current_user.id).first()

    return render_template("profile.html", stocks=owned_stocks, form=form, account=has_account)

@views.route("/sell_stock", methods=["POST", "GET"])
@login_required
def sell_stock_page():
    """
    Sell stock page route for the web application.

    Displays a form for the user to input the stock ticker and the amount of shares they want to sell. Upon submission, the function checks if the user has enough shares of the stock to sell. If they do, it subtracts the sold amount of shares from their stock holdings, updates the database accordingly, and redirects the user to the profile page. If they do not have enough shares to sell, the function displays an error message.

    Requires the user to be logged in to access the page. Uses the `SellStockForm` FlaskForm to validate the form data.

    Returns:
        A rendered HTML template, including the `SellStockForm` and appropriate messages.
    """

    form = SellStockForm()

    if form.validate_on_submit():
        stock_ticker = form.stock_ticker.data.upper()
        stock_shares = form.shares.data

        if current_user.can_sell(stock_ticker=stock_ticker, shares=stock_shares):
            owned_stock = Stock.query.filter_by(user_id=current_user.id, ticker=stock_ticker).first()

            # update the stock
            old_total_shares = owned_stock.shares
            new_total_shares = old_total_shares - stock_shares

            if new_total_shares == 0: # if he sold all of his stocks
                db.session.delete(owned_stock)

            else:
                old_average_price = owned_stock.average_price
                new_average_price = (owned_stock.cost_basis - (stock_shares * old_average_price)) / new_total_shares

                new_cost_basis = new_average_price * new_total_shares

                owned_stock.shares = new_total_shares
                owned_stock.average_price = new_average_price
                owned_stock.cost_basis = new_cost_basis

            # update the balance
            account = Account.query.filter_by(user_id=current_user.id).first()
            current_stock_price = get_stock_price_by_ticker(stock_ticker)
            account.balance += stock_shares * current_stock_price

            db.session.commit()
            flash(message=f"You successfully sold {stock_shares} amount of shares at {owned_stock.average_price}$", category="success")

            return redirect(url_for("views.profile_page"))
    
    return render_template("sell_stock.html", form=form)

