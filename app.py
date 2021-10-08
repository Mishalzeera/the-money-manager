import os
import json
from functions import *
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from flask import (
    Flask, render_template, request, flash, redirect, session, url_for)
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
def index():
    if "user" not in session:
        return render_template("index.html", user=" of Great Future Wealth.")
    else:
        return render_template("index.html", user=session["user"])


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username exists
        existing_user = mongo.db.users.find_one(
            {"name": request.form.get("name").lower()})
        if existing_user:
            flash("Username exists!")
            return redirect(url_for('register'))
        # create dictionary for new user
        register_user = {
           "name": request.form.get("name").lower(),
           "password": generate_password_hash(request.form.get("password"))
        }
        #  create dictionary for new starting month
        start_credit_to_int = euros_to_cents(request.form.get("starting-credit"))
        user_overheads_to_int = euros_to_cents(request.form.get("user-overheads"))
        start_month = {
            "name": request.form.get("name").lower(),
            "credit": start_credit_to_int,
            "user_overheads": user_overheads_to_int,
            "income_this_month": 0,
            "spent_this_month": 0,
            "spent_on_overheads": 0,
            "spent_on_extras": 0,
            "overheads_to_be_paid": 0,
            "tax_to_set_aside": 0,
            "suggested_savings_amount": 0,
            "disposable_income": 0
        }
        
        # send dictionaries to Mongo

        mongo.db.users.insert_one(register_user)
        mongo.db.current_month.insert_one(start_month)

        # put user into session cookie
        session["user"] = request.form.get("name").lower()
        flash("Registration Successful")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists
        existing_user = mongo.db.users.find_one(
            {"name": request.form.get("name").lower()})
        
        if existing_user:
            # check password
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("name").lower()
                    flash("Welcome, {}".format(request.form.get("name")))
                    return redirect(url_for('profile', username=session["user"]))
            else:
                flash("Incorrect Username or Password")
                return redirect(url_for('login'))

        else:
            # no such user
            flash("Incorrect Username or Password")
            return redirect(url_for('login'))

    return render_template("login.html")


@app.route("/profile/<username>")
def profile(username):
    money = mongo.db.current_month.find_one({"name": session["user"]})
    return render_template("profile.html", user=session["user"], money=money)


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5500")),
        debug=True
    )
