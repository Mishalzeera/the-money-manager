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
    # get the dictionary from the database in cents
    money_cents = mongo.db.current_month.find_one({"name": session["user"]})
    # iterate through the contents checking types for integers
    money={}
    # new empty dictionary
    for key, value in money_cents.items():
        if type(value) == int:
            # update the new dictionary using helper function from functions.py
            money.update({key: cents_to_euros(value)})
            # send the new dictionary to the profile template
    return render_template("profile.html", user=session["user"], money=money)


@app.route("/invoice", methods=["GET", "POST"])
def invoice():
    if request.method == "POST":
        
        return redirect(url_for('profile', username=session['user']))

    return render_template("invoice.html")

@app.route("/edit_invoice", methods=["GET", "POST"])
def edit_invoice(invoice_id):
    return render_template("edit_invoice.html")

@app.route("/wishlist", methods=["GET","POST"])
def wishlist():

    if request.method == 'POST':
        # convert currency to cents
        cost_of_item = euros_to_cents(request.form.get("wish_cost"))
        # create a wishlist dictionary
        wishlist_item = {
            "name": session["user"],
            "wish_name": request.form.get("wish_name").lower(),
            "wish_cost": cost_of_item,
            "wish_description": request.form.get("wish_description"),
            "is_affordable": False
        }
        # send dictionary to the database
        mongo.db.wishlist.insert_one(wishlist_item)
        flash("Item successfully added")
        return redirect(url_for('wishlist'))


            # get user wishlist from db
    wishlist = mongo.db.wishlist.find({"name": session["user"]})
    
    return render_template("wishlist.html", wishlist=wishlist)
    

@app.route("/delete_wish/<wish>", methods=["GET", "POST"])
def delete_wish(wish):
    if request.method == "POST":
        wish_to_delete = mongo.db.wishlist.find_one({"_id": ObjectId(wish)})
        mongo.db.wishlist.remove(wish_to_delete)
        flash("Wish deleted!")
        return redirect(url_for('wishlist'))
    else: 
        return redirect(url_for('wishlist'))


@app.route("/edit_wish/<wish>", methods=["GET", "POST"])
def edit_wish(wish):
    if request.method == "POST":
        wish_to_edit = mongo.db.wishlist.find_one({"_id": ObjectId(wish)})
        return render_template("edit_wish.html", wish=wish_to_edit)
    else: 
        return redirect(url_for('wishlist'))


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for('login'))


@app.route("/settings")
def settings():
    return render_template("settings.html", user=session["user"])

@app.route("/delete_account")
def delete_account():
    mongo.db.users.remove({"name": session["user"]})
    mongo.db.current_month.remove({"name": session["user"]})
    flash("May Allah enrich all your days. Your account has been deleted.")
    session.clear()
    return redirect('login')


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5500")),
        debug=True
    )
