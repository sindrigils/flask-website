from flask import render_template, redirect, url_for, request, Blueprint, flash
from flask_login import login_required, current_user
from website import db
from website.models import Stock
from website.forms import StockTickerForm, PurchaseStockForm, SellStockForm
from website.stock.stock_models import get_stock_price_by_ticker

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
        stock_price = get_stock_price_by_ticker(stock_ticker)
    
        return render_template("get_stock.html", form=form, stock_ticker=stock_ticker, stock_price=stock_price)
    
    return render_template("get_stock.html", form=form)


@views.route("/buy_stock<stock_ticker>/<stock_price>", methods=["POST", "GET"])
@login_required
def buy_stock_page(stock_ticker, stock_price):
    form = PurchaseStockForm()

    if form.validate_on_submit():
        buy_stock = Stock(
            ticker=stock_ticker,
            bought_price=stock_price,
            shares=form.shares.data,
            user_id=current_user.id)
        
        db.session.add(buy_stock)
        db.session.commit()
        flash(message=f"You have bought the stock successfully!", category="success")

        return redirect(url_for("views.stock_ticker_page"))

    return render_template("buy_stock.html", form=form, stock_ticker=stock_ticker, stock_price=stock_price)



@views.route("/profile")
@login_required
def profile_page():
    owned_stocks = Stock.query.filter_by(user_id=current_user.id)
    return render_template("profile.html", stocks=owned_stocks)