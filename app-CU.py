import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash


from helpers import apology, login_required, lookup, usd

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


@app.route("/")
@login_required
def index():
    reader = db.execute(
        f"SELECT DISTINCT stock, qnt FROM ownage WHERE {session['user_id']} = ownage.id")
    total = 0
    for rea in reader:
        rea['value'] = rea['qnt'] * lookup(rea['stock'])['price']
        total = total + rea['value']
        rea['value'] = usd(rea['value'])
    total = usd(total)
    return render_template("index.html", reader=reader, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        symbol = request.form['symbol']
        qnt = request.form['shares']
        try:
            int(qnt)
        except:
            return apology("Insert an integer")
        if int(qnt) < 0:
            return apology("Insert an integer")
        result = lookup(symbol)
        if result is None:
            return apology("Symbol not found.")
        qnt = int(qnt)
        minusTot = qnt * result['price']
        userTot = db.execute(f"SELECT cash FROM users WHERE {session['user_id']} = users.id")
        userTot = userTot[0]['cash'] - minusTot
        if userTot < 0:
            return apology("You're too broke.")
        db.execute(f"UPDATE users SET cash={userTot} WHERE {session['user_id']} = users.id")
        db.execute(
            f"INSERT INTO history (id, stock, price, date, qnt) VALUES ({session['user_id']}, '{symbol}', -{minusTot}, '{datetime.datetime.now()}', {qnt})")

        db.execute(f"INSERT INTO ownage (id, stock) VALUES ({session['user_id']}, '{symbol}')")
        nqnt = db.execute(
            f"SELECT qnt FROM ownage WHERE stock = '{symbol}' AND {session['user_id']} = ownage.id")
        nqnt = qnt + nqnt[0]['qnt']
        # nqnt = int(qnt) + nqnt[0]['qnt']
        db.execute(
            f"UPDATE ownage SET qnt={nqnt} WHERE {session['user_id']} = ownage.id AND stock='{symbol}'")
        minusTot = usd(minusTot)
        return index()
    return render_template("buy.html", symbol=0, minusTot=0)


@app.route("/history")
@login_required
def history():
    reader = db.execute(
        f"SELECT stock, price, qnt, date FROM history WHERE {session['user_id']} = history.id ORDER BY date DESC")
    return render_template("history.html", reader=reader)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        result = lookup(request.form['symbol'])
        if request.form['symbol'] == '':
            return apology("Insert Symbol")
        if result is None:
            return apology("Insert valid symbol")
        stuff = lookup(request.form['symbol'])
        stuff['price'] = usd(stuff['price'])
        return render_template("quoted.html", stuff=stuff)
    return render_template("quote.html", )


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        if request.form['password'] == '':
            return apology("Insert a password")
        if request.form['username'] == '':
            return apology("Insert an username")
        if request.form['password'] != request.form['confirmation']:
            return apology("Incorrect Match")
        if request.form['username'].isspace():
            return apology("Missing Username")
        if request.form['password'].isspace():
            return apology("Missing Password")
        pash = generate_password_hash(request.form['password'])
        if db.execute(f"SELECT username FROM users WHERE username='{request.form['username']}'"):
            return apology("This user already exists")
        db.execute(
            f"INSERT INTO users (username, hash) VALUES ('{request.form['username']}', '{pash}')")
    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":

        symbol = request.form['symbol']
        qnt = request.form['shares']
        result = lookup(symbol)
        try:
            int(qnt)
        except:
            return apology("Insert an integer")
        if int(qnt) < 0:
            return apology("Insert an integer")
        result = lookup(symbol)
        if result is None:
            return apology("Symbol not found.")
        minusTot = int(qnt) * result['price']
        max = db.execute(f"SELECT qnt FROM ownage WHERE {session['user_id']} = ownage.id")
        if int(qnt) > max[0]['qnt']:
            return apology("You dont have this many stocks")
        userTot = db.execute(f"SELECT cash FROM users WHERE {session['user_id']} = users.id")
        userTot = userTot[0]['cash'] + minusTot
        db.execute(f"UPDATE users SET cash={userTot} WHERE {session['user_id']} = users.id")

        db.execute(
            f"INSERT INTO history (id, stock, price, date, qnt) VALUES ({session['user_id']}, '{symbol}', +{minusTot}, '{datetime.datetime.now()}', {qnt})")
        nqnt = db.execute(
            f"SELECT qnt FROM ownage WHERE stock = '{symbol}' AND {session['user_id']} = ownage.id")
        if len(nqnt) == 0:
            db.execute(f"INSERT INTO ownage (id, stock) VALUES ({session['user_id']}, '{symbol}')")
        nqnt = nqnt[0]['qnt'] - int(qnt)
        if nqnt == 0:
            db.execute(f"DELETE FROM ownage WHERE stock='{symbol}'")
        db.execute(
            f"UPDATE ownage SET qnt={nqnt} WHERE {session['user_id']} = ownage.id AND stock='{symbol}'")
        minusTot = usd(minusTot)
        return render_template("sell.html", symbol=symbol, minusTot=minusTot)
    return render_template("sell.html", symbol=0, minusTot=0)


@app.route("/mocash", methods=["GET", "POST"])
@login_required
def newcash():
    if request.method == "POST":
        ccash = db.execute(f"SELECT cash FROM users WHERE {session['user_id']}=users.id")
        ncash = float(request.form['money']) + ccash[0]['cash']
        db.execute(f"UPDATE users SET cash={ncash} WHERE {session['user_id']}=users.id")
    return render_template("mocash.html")
