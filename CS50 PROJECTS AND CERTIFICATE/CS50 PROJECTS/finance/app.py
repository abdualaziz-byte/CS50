import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd
from datetime import datetime

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():

    if request.method == "POST":

        id = session["user_id"]

        balance = db.execute(
            "SELECT cash FROM users WHERE id = ?", id
        )[0]["cash"]

        try:
            funds = float(request.form.get("addfunds"))
        except (TypeError, ValueError):
            return apology("must provide a valid amount", 400)

        if funds <= 0:
            return apology("amount must be greater than 0", 400)

        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?",
            balance + funds,
            id
        )

        return redirect("/history")

    if request.method == "GET":

        id = session["user_id"]

        balance = db.execute(
            "SELECT cash FROM users WHERE id = ?", id
        )[0]["cash"]

        portfolio = db.execute(
            """
            SELECT symbol, SUM(shares) AS shares
            FROM portfolio
            WHERE user_id = ?
            GROUP BY symbol
            """,
            id
        )

        for x in portfolio:
            x["price"] = lookup(x["symbol"])["price"]

        return render_template(
            "index.html",
            balance=balance,
            portfolio=portfolio
        )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():

    if request.method == "GET":
        return render_template("buy.html")

    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("must provide name of symbol", 400)

        elif not request.form.get("shares"):
            return apology("must provide amount of shares to buy", 400)

        try:
            amountOstocks = int(request.form.get("shares"))
        except ValueError:
            return apology("must provide a whole number of shares", 400)

        if amountOstocks < 1:
            return apology(
                "must provide amount of shares higher or equal to 1",
                400
            )

        symbol = request.form.get("symbol").upper()

        if not lookup(symbol):
            return apology("stock doesnt exist", 400)

        id = session["user_id"]

        balance = db.execute(
            "SELECT cash FROM users WHERE id = ?", id
        )[0]["cash"]

        priceOstock = lookup(symbol)["price"]

        stockstotal = priceOstock * amountOstocks

        newbalance = balance - stockstotal

        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if newbalance < 0:
            return apology("not enough funds", 400)

        else:

            db.execute(
                "UPDATE users SET cash = ? WHERE id = ?",
                newbalance,
                id
            )

            db.execute(
                """
                INSERT INTO portfolio
                (user_id, symbol, shares, price, date, transaction_type)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                id,
                symbol,
                amountOstocks,
                stockstotal,
                time,
                "BUY"
            )

    return redirect("/buy")


@app.route("/history", methods=["GET"])
@login_required
def history():

    if request.method == "GET":

        id = session["user_id"]

        history = db.execute(
            "SELECT * FROM portfolio WHERE user_id = ?",
            id
        )

        return render_template(
            "history.html",
            history=history
        )


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    session.clear()

    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must provide username", 400)

        elif not request.form.get("password"):
            return apology("must provide password", 400)

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?",
            request.form.get("username")
        )

        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"],
            request.form.get("password")
        ):
            return apology(
                "invalid username and/or password",
                403
            )

        session["user_id"] = rows[0]["id"]

        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    session.clear()

    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "GET":
        return render_template("quote.html")

    if not request.form.get("symbol"):
        return apology("must provide symbol", 400)

    symbol = request.form.get("symbol").upper()

    stock = lookup(symbol)

    if not stock:
        return apology("symbol does not exist", 400)

    return render_template(
        "stock.html",
        name=stock["name"],
        price=stock["price"],
        symbol=stock["symbol"]
    )

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must provide username", 400)

        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif not request.form.get("confirmation"):
            return apology(
                "must provide password confirmation",
                400
            )

        elif request.form.get("confirmation") != request.form.get("password"):
            return apology(
                "passwords don't match",
                400
            )

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?",
            request.form.get("username")
        )

        if len(rows) > 0:
            return apology(
                "username is already taken",
                400
            )

        db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)",
            request.form.get("username"),
            generate_password_hash(
                request.form.get("password")
            )
        )

        rows = db.execute(
            "SELECT id FROM users WHERE username = ?",
            request.form.get("username")
        )

        session["user_id"] = rows[0]["id"]

        return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():

    if request.method == "GET":
        return render_template("sell.html")

    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("must provide name of symbol", 400)

        elif not request.form.get("shares"):
            return apology("must provide amount of shares to sell", 400)

        try:
            amountOstocks = int(request.form.get("shares"))
        except ValueError:
            return apology(
                "must provide a whole number of shares",
                400
            )

        if amountOstocks < 1:
            return apology(
                "must provide amount of shares higher or equal to 1",
                400
            )

        symbol = request.form.get("symbol").upper()

        if not lookup(symbol):
            return apology("stock doesnt exist", 400)

        id = session["user_id"]

        balance = db.execute(
            "SELECT cash FROM users WHERE id = ?",
            id
        )[0]["cash"]

        priceOstock = lookup(symbol)["price"]

        stockstotal = priceOstock * amountOstocks

        newbalance = balance + stockstotal

        stockswantedtosell = db.execute(
            """
            SELECT SUM(shares) AS shares
            FROM portfolio
            WHERE user_id = ? AND symbol = ?
            """,
            id,
            symbol
        )[0]["shares"]

        if stockswantedtosell is None:
            stockswantedtosell = 0

        time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        if stockswantedtosell < amountOstocks:
            return apology(
                "not enough stocks",
                400
            )

        else:

            db.execute(
                "UPDATE users SET cash = ? WHERE id = ?",
                newbalance,
                id
            )

            db.execute(
                """
                INSERT INTO portfolio
                (user_id, symbol, shares, price, date, transaction_type)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                id,
                symbol,
                -amountOstocks,
                stockstotal,
                time,
                "SELL"
            )

    return redirect("/sell")
