import os
import requests
import hashlib

from flask import Flask, session, request, render_template, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

#key = "ev1BloPVJzToGutMhjI5g"
#res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": key, "isbns": "9781632168146"})
#print(res.json())

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/login")
def login():
    return render_template("auth.html", main="Log In", navs={"Register": "register"})

@app.route("/register")
def register():
    return render_template("auth.html", main="Register", navs={"Log In": "login"})

@app.route("/authenticate", methods=["POST"])
def authenticate():
    username = request.form.get("username")
    password = request.form.get("password")
    auth_type = request.form.get("auth_type")

    #Register
    if auth_type is "Register":
        db.execute("INSERT INTO flights (username, passhash) VALUES (:username, :passhash)",
            {"username": username, "passhash": hashlib.md5(password.encode()).hexdigest()})
        db.commit()

    #Check if user exists
    if db.execute("SELECT * FROM users WHERE username = :username AND passhash = :passhash", 
        {"username": username, "passhash": hashlib.md5(password.encode()).hexdigest()}).rowcount == 0:
        return redirect(url_for('login'))

    session["username"] = username
    return redirect(url_for('index'))
    

@app.route("/")
def index():
    if session.get("username") is None:
        return redirect(url_for('login'))
    else:
        return render_template("index.html", main="Home", navs=["Log Out"])