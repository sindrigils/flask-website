from flask import render_template, redirect, url_for, request, Blueprint, flash
from flask_login import login_required, current_user
from website import db
from website.models import Stock
from website.forms import StockTickerForm, PurchaseStockForm, SellStockForm
from website.stock.stock_models import get_stock_price_by_ticker, plot_a_graph

views = Blueprint("views", __name__)

@views.route("/")
def home_page():
    return render_template("home.html")

@views.route("/stock_ticker", methods=["POST", "GET"])
@login_required
def stock_ticker_page():
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
    form = PurchaseStockForm()
    filename = plot_a_graph(stock_ticker)

    if form.validate_on_submit():
        buy_stock = Stock(
            ticker=stock_ticker,
            average_price=stock_price,
            shares=form.shares.data,
            user_id=current_user.id)
        
        owned_stock = Stock.query.filter_by(user_id=current_user.id, ticker=stock_ticker).first() # check if the user already owns this stock if so than add up his shares
        if owned_stock:
            old_total_shares = owned_stock.shares
            old_average_price = owned_stock.average_price

            new_total_shares = old_total_shares + form.shares.data
            new_average_price = (old_average_price * old_total_shares + float(form.shares.data) * float(stock_price)) / new_total_shares

            owned_stock.shares = new_total_shares
            owned_stock.average_price = new_average_price
            db.session.commit()

        else:
            db.session.add(buy_stock)
            db.session.commit()

        flash(message=f"You have bought the stock successfully!", category="success")
        return redirect(url_for("views.stock_ticker_page"))

    return render_template("buy_stock.html", form=form, stock_ticker=stock_ticker, stock_price=stock_price, filename=filename)



@views.route("/profile")
@login_required
def profile_page():
    owned_stocks = Stock.query.filter_by(user_id=current_user.id)

    return render_template("profile.html", stocks=owned_stocks)

@views.route("/sell_stock", methods=["POST", "GET"])
@login_required
def sell_stock_page():
    form = SellStockForm()

    if form.validate_on_submit():
        stock_ticker = form.stock_ticker.data
        stock_shares = form.shares.data

        if current_user.can_sell(stock_ticker=stock_ticker, shares=stock_shares):
            stock = Stock.query.filter_by(user_id=current_user.id, ticker=stock_ticker).first()

            stock.shares = stock.shares - stock_shares
            db.session.commit()
            flash(message=f"You successfully sold {stock_shares} amount of shares at {stock.average_price}$", category="success")

            return redirect(url_for("views.profile_page"))
    
    return render_template("sell_stock.html", form=form)

