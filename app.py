from datetime import datetime
import os
from functools import wraps
import inspect
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


def ensure_user(route):
    # decorator for routes that ensure access only to a logged in user
    # uses "wraps" function from "functools"
    @wraps(route)
    def wrapper_function(*args, **kwargs):
        if 'user' not in session:
            flash("You must be logged in to access that page.")
            return redirect(url_for('login'))
        else:
            return route(*args, **kwargs)
    return wrapper_function


def calculate_disposable_income():
    # to be inserted after any income/expense calculation
    # takes overheads, tax and suggested savings, adds them and subtracts the sum from credit
    # create a user key 
    user_key = {"name": session['user']}
    # get the current month object
    current_month = mongo.db.current_month.find_one(user_key)
    # get the credit from the object
    credit = current_month['credit']
    # get the overheads to be paid
    overheads_to_be_paid = current_month['overheads_to_be_paid']
    # get the tax to set aside
    tax_to_set_aside = current_month['tax_to_set_aside']
    # get the suggested savings amount
    suggested_savings_amount = current_month['suggested_savings_amount']
    # calculate the disposable income
    disposable_income = credit - (overheads_to_be_paid + tax_to_set_aside + suggested_savings_amount)
    # ...and update the database with the amount
    mongo.db.current_month.update_one(user_key, {"$set": {"disposable_income": disposable_income}})


def create_income_record(db_object):
    # creates a record of every income, for the user_history.html page
    # create user key
    user_key = {"name": session['user']}
    # get a real time date stamp for the object
    datestamp = datetime.today().strftime('%d-%m-%Y')
    # get the amount from the argument-object
    amount = db_object['amount']
    # get the recipient from the argument-object
    recipient = db_object['invoice_recipient']
    # get the tax if applicable
    tax = db_object['tax']
    # get the current credit from the users current month object
    credit = mongo.db.current_month.find_one(user_key)['credit']
    # create a record object
    
    record = {
        "name": session['user'],
        "date": datestamp,
        "amount": amount,
        "recipient": recipient,
        "tax": tax,
        "credit_after": credit,
        "type": "income"
    }
    # insert the object into the database
    mongo.db.in_out_history.insert_one(record)


def create_modified_income_record(db_object):
    # creates a record of every modified income
    # create user key
    user_key = {"name": session['user']}
    # get a real time date stamp for the object
    datestamp = datetime.today().strftime('%d-%m-%Y')
    # get the amount from the argument-object
    amount = db_object['amount']
    # get the recipient from the argument-object
    recipient = db_object['invoice_recipient']
    # get the tax if applicable
    tax = db_object['tax']
    # get the current credit from the users current month object
    credit = mongo.db.current_month.find_one(user_key)['credit']
    # create a record object
    
    record = {
        "name": session['user'],
        "date": datestamp,
        "amount": amount,
        "recipient": recipient,
        "tax": tax,
        "credit_after": credit,
        "type": "income-modified"
    }

    # insert the object into the database
    mongo.db.in_out_history.insert_one(record)


def create_deleted_income_record_part_one(db_object):
    # creates a record of every deleted income
    # since the credit can only be calculated after the deletion
    # the function is in two parts, one before the database manipulation
    # and one after, to insert the "credit after" amount
    # get datestamp
    datestamp = datetime.today().strftime('%d-%m-%Y')
    # get a hours minutes seconds stamp to match records correctly
    now  = datetime.now() 
    # create a timestamp
    timestamp = now.strftime("%H:%M:%S")
    # get the argument-object amount
    amount = db_object['amount']
    # get the argument-object recipient
    recipient = db_object['invoice_recipient']
    # get tax if applicable
    tax = db_object['tax']
    # create a record
    
    record = {
        "name": session['user'],
        "timestamp": timestamp,
        "date": datestamp,
        "amount": amount,
        "recipient": recipient,
        "tax": tax,
        "type": "income-deleted"
    }
    # insert it into the database
    mongo.db.in_out_history.insert_one(record)


def create_deleted_income_record_part_two():
    # updates the object created in part_one with the recalculated credit_after
    # create user key
    user_key = {"name": session['user']}
    # get current credit
    credit = mongo.db.current_month.find_one(user_key)['credit']
    # find the current timestamp
    now  = datetime.now() 
    # create a formatted timestamp to match the database
    timestamp = now.strftime("%H:%M:%S")
    # using the timestamp, get and update the correct record
    mongo.db.in_out_history.update_one({"timestamp": timestamp}, {"$set": {"credit_after": credit}})


def create_expense_record(db_object):
    # creates a record of every expense
    # create a user key
    user_key = {"name": session['user']}
    # get a datestamp for the new object
    datestamp = datetime.today().strftime('%d-%m-%Y')
    # get the amount from the argument-object
    amount = db_object['amount']
    # get the "overheads" or "extras" type - not to be confused with the new 
    # "type" key which is a hard coded string for an "if else" in the template
    for_type = db_object["type"]
    # get the recipient from the argument-object
    recipient = db_object['recipient']
    # get the current credit from the current month object
    credit = mongo.db.current_month.find_one(user_key)['credit']
    # create a new record
    
    record = {
        "name": session['user'],
        "date": datestamp,
        "amount": amount,
        "for": for_type,
        "recipient": recipient,
        "credit_after": credit,
        "type": "expense"
    }

    # insert the new object into the database
    mongo.db.in_out_history.insert_one(record)


def create_modified_expense_record(db_object):
    # creates a record of every modified expense
    # create a user key
    user_key = {"name": session['user']}
    # create a datestamp for the record
    datestamp = datetime.today().strftime('%d-%m-%Y')
    # get the amount from the "abject-orgument" (sorry)
    amount = db_object['amount']
    # get the "overheads" vs "extras" type from the argument-object
    # not to be confused with the hard coded "type" string for the
    # template "if else" structure
    for_type = db_object["type"]
    # get the recipient from the argument-object
    recipient = db_object['recipient']
    # get the current month object credit
    credit = mongo.db.current_month.find_one(user_key)['credit']
    # create a record

    record = {
        "name": session['user'],
        "date": datestamp,
        "amount": amount,
        "for": for_type,
        "recipient": recipient,
        "credit_after": credit,
        "type": "expense-modified"
    }

    # insert the record into the database
    mongo.db.in_out_history.insert_one(record)


def create_deleted_expense_record_part_one(db_object):
    # creates a record of every deleted expense
    # in two parts, so that the updated credit can be inserted 
    # after the database is manipulated
    # get a datestamp for the new record
    datestamp = datetime.today().strftime('%d-%m-%Y')
    # get now for the timestamp
    now  = datetime.now() 
    # create a timestamp for part two to target the correct object
    timestamp = now.strftime("%H:%M:%S")
    # get the "overheads" vs "extras" type from the argument-object
    # not to be confused with the hard coded "type" string for the
    # template to use in an "if else" statement
    for_type = db_object["type"]
    # get the amount from the argument-object
    amount = db_object['amount']
    # get the recipient
    recipient = db_object['recipient']
    # create a record
    
    record = {
        "name": session['user'],
        "date": datestamp,
        "timestamp": timestamp,
        "amount": amount,
        "for": for_type,
        "recipient": recipient,
        "type": "expense-deleted"
    }

    # insert it into the database
    mongo.db.in_out_history.insert_one(record)


def create_deleted_expense_record_part_two():
    # allows for updating the object created in part_one with the recalculated credit_after
    # create a user key
    user_key = {"name": session['user']}
    # get the current credit from the current month object
    credit = mongo.db.current_month.find_one(user_key)['credit']
    # get a timestamp for hours minutes seconds
    now  = datetime.now() 
    # create a variable from it to match with the correct record
    timestamp = now.strftime("%H:%M:%S")
    # update the record created in the first part with the credit_after
    mongo.db.in_out_history.update_one({"timestamp": timestamp}, {"$set": {"credit_after": credit}})


@app.route("/")
def index():
    # handles when the user navigates to the site initially
    # if user not in session, goes to login
    if "user" not in session:
        return redirect(url_for('login'))
    else:
    # goes to the users profile page
        return render_template("profile.html", user=session["user"])


@app.route("/register", methods=["GET", "POST"])
def register():
    # allows the user to register a new account
    if request.method == "POST":
        # check if username exists
        existing_user = mongo.db.users.find_one(
            {"name": request.form.get("name").lower()})
        if existing_user:
            flash("Username exists!")
            return redirect(url_for('register'))
        # create dictionary for new user
        # uses the very handy generate password hash from Werkzeug
        register_user = {
           "name": request.form.get("name").lower(),
           "password": generate_password_hash(request.form.get("password"))
        }
        #  create dictionary for new starting month
        # sets the starting credit and the users overheads, defined by the user
        start_credit_to_int = euros_to_cents(request.form.get("starting-credit"))
        user_overheads_to_int = euros_to_cents(request.form.get("user-overheads"))

        # handling the tax rate, a key part of the app
        # if no tax rate is entered, amount is set to the
        # Netherlands default
        if request.form.get("tax_rate") == '':
            tax_rate_to_int = 121
        else:
        # makes a concatenated string out of the number entered by the user
        # allowing a "1" to be inserted before, which puts the tax rate into
        # the most useable format by the database
            tax_rate_to_string = "1" + str(request.form.get("tax_rate"))
            tax_rate_to_int = int(tax_rate_to_string)
        
        # create a starting month object
        start_month = {
            "name": request.form.get("name").lower(),
            "credit": start_credit_to_int,
            "user_overheads": user_overheads_to_int,
            "income_this_month": 0,
            "spent_this_month": 0,
            "spent_on_overheads": 0,
            "spent_on_extras": 0,
            "overheads_to_be_paid": user_overheads_to_int,
            "tax_rate": tax_rate_to_int,
            "tax_to_set_aside": 0,
            "suggested_savings_amount": 0,
            "disposable_income": 0,
            "preferred_theme": "dark"
        }
        
        # send dictionaries to Mongo

        mongo.db.users.insert_one(register_user)
        mongo.db.current_month.insert_one(start_month)

        # put user into a session cookie
        session["user"] = request.form.get("name").lower()
        # puts user tax rate into a session cookie
        session["tax_rate"] = tax_rate_to_int
        # create cookie for display theme, defaults to dark
        session["theme"] = "dark"
        # give some user feedback
        flash("Registration Successful")
        # go to the new users profile
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
                    session["theme"] = mongo.db.current_month.find_one({"name": session['user']})["preferred_theme"]
                    session["tax_rate"] = mongo.db.current_month.find_one({"name": session['user']})["tax_rate"]
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
@ensure_user
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


@app.route("/invoice")
@ensure_user
def invoice():
    user_key = {"name": session['user']}
    invoices = mongo.db.invoices.find(user_key) 
    return render_template("invoice.html", invoices=invoices)


@app.route("/add_invoice", methods=["GET", "POST"])
@ensure_user
def add_invoice():
    if request.method == "POST":
        # set the tax rate variable
        tax_rate = session["tax_rate"]
        # convert the currency from euros to cents
        invoice_amount_cents = euros_to_cents(request.form.get("amount_invoiced"))
        # calculate the amount to set aside for taxes
        invoice_tax_amount = round(new_invoice_tax(invoice_amount_cents, tax_rate))
        # calculate the profit amount
        post_tax_income = round(new_invoice_income(invoice_amount_cents, tax_rate))
        # create a new invoice object
        new_invoice = {
            "name": session['user'],
            "date": request.form.get("invoice_date"),
            "invoice_number": request.form.get("invoice_number").lower(),
            "invoice_recipient": request.form.get("invoice_recipient").lower(),
            "amount": invoice_amount_cents,
            "invoice_tax_amount": invoice_tax_amount,
            "post_tax_income": post_tax_income,
            "tax": request.form.get("tax"),
            "comments": request.form.get("comments")
        }
        # insert new object
        mongo.db.invoices.insert_one(new_invoice)
        # create reusable key
        user_key = {"name": session['user']}
        # get credit, add new income
        if request.form.get("tax") == "on":
            # in the case of taxeable income
            credit = mongo.db.current_month.find_one(user_key)["credit"]
            new_credit = invoice_amount_cents + credit
            # get tax_to_set_aside and add new tax amount
            tax_to_set =  mongo.db.current_month.find_one(user_key)["tax_to_set_aside"]
            new_tax = tax_to_set + invoice_tax_amount
            # update credit and tax_to_set_aside fields
            mongo.db.current_month.update_one(user_key, {"$set": {"credit": new_credit}})
            mongo.db.current_month.update_one(user_key, {"$set": {"tax_to_set_aside": new_tax}})
            # get income_this_month
            old_income = mongo.db.current_month.find_one(user_key)["income_this_month"]
            new_income = old_income + post_tax_income
            # add to income_this_month
            mongo.db.current_month.update_one(user_key, {"$set": {"income_this_month": new_income}})
            # get suggested_savings_amount
            savings = mongo.db.current_month.find_one(user_key)["suggested_savings_amount"]
            suggested_savings = round(savings + (post_tax_income * .2))
            # add to suggested savings this month
            mongo.db.current_month.update_one(user_key, {"$set": {"suggested_savings_amount": suggested_savings}})
        else:
            # in the case of non-taxeable income
            # get credit, add new income 
            credit = mongo.db.current_month.find_one(user_key)["credit"]
            new_credit = credit + invoice_amount_cents
            mongo.db.current_month.update_one(user_key, {"$set": {"credit": new_credit}})
            # get income_this_month
            old_income = mongo.db.current_month.find_one(user_key)["income_this_month"]
            new_income = old_income + invoice_amount_cents
            # add to income_this_month
            mongo.db.current_month.update_one(user_key, {"$set": {"income_this_month": new_income}})
            # get suggested savings, add suggested savings
            savings = mongo.db.current_month.find_one(user_key)["suggested_savings_amount"]
            suggested_savings = round(savings + (invoice_amount_cents * .2))
            mongo.db.current_month.update_one(user_key, {"$set": {"suggested_savings_amount": suggested_savings}})
        # calculate disposable income
        calculate_disposable_income()
        # create record using the new object as an argument
        create_income_record(new_invoice)
        # provide confirmation to user:
        flash("Invoice successfully added!")
        return redirect(url_for('profile', username=session['user']))

    return render_template("add_invoice.html")


@app.route("/edit_invoice/<invoice_id>", methods=["GET", "POST"])
@ensure_user
def edit_invoice(invoice_id):
    if request.method == "POST":
        # recalculate credit and relevant fields before updating
        # set tax rate
        tax_rate = session["tax_rate"]
        # get credit, income_this_month, suggested_savings_amount, tax_to_set_aside
        user_key = {"name": session['user']}
        current_month = mongo.db.current_month.find_one(user_key)
        credit_before = current_month["credit"]
        income_before = current_month["income_this_month"]
        suggested_savings_before = current_month["suggested_savings_amount"]
        tax_before = current_month["tax_to_set_aside"]
        # get old invoice amount
        old_invoice = mongo.db.invoices.find_one({"_id": ObjectId(invoice_id)})
        old_amount = old_invoice["amount"]
        # set variables for following conditional
        # calculate the amount previously set aside for taxes
        invoice_tax_amount = round(new_invoice_tax(old_amount, tax_rate))
        # calculate the profit amount
        post_tax_income = round(new_invoice_income(old_amount, tax_rate))
        # check whether the invoice was taxeable, recalculate all factors
        if old_invoice['tax'] == "on":
            # in the case of taxeable income
            credit = mongo.db.current_month.find_one(user_key)["credit"]
            new_credit = credit - old_amount
            # get tax_to_set_aside and add new tax amount
            tax_to_set =  mongo.db.current_month.find_one(user_key)["tax_to_set_aside"]
            new_tax = tax_to_set - invoice_tax_amount
            # update credit and tax_to_set_aside fields
            mongo.db.current_month.update_one(user_key, {"$set": {"credit": new_credit}})
            mongo.db.current_month.update_one(user_key, {"$set": {"tax_to_set_aside": new_tax}})
            # get income_this_month
            old_income = mongo.db.current_month.find_one(user_key)["income_this_month"]
            new_income = old_income - post_tax_income
            # update income_this_month
            mongo.db.current_month.update_one(user_key, {"$set": {"income_this_month": new_income}})
            # get suggested_savings_amount
            savings = mongo.db.current_month.find_one(user_key)["suggested_savings_amount"]
            suggested_savings = round(savings - (post_tax_income * .2))
            # add to suggested savings this month
            mongo.db.current_month.update_one(user_key, {"$set": {"suggested_savings_amount": suggested_savings}})
        else:
            # in the case of non-taxeable income
            # get credit, subtract old income 
            credit = mongo.db.current_month.find_one(user_key)["credit"]
            new_credit = credit - old_amount
            mongo.db.current_month.update_one(user_key, {"$set": {"credit": new_credit}})
            # get income_this_month
            old_income = mongo.db.current_month.find_one(user_key)["income_this_month"]
            new_income = old_income - old_amount
            # add to income_this_month
            mongo.db.current_month.update_one(user_key, {"$set": {"income_this_month": new_income}})
            # get suggested savings, add suggested savings
            savings = mongo.db.current_month.find_one(user_key)["suggested_savings_amount"]
            suggested_savings = round(savings - (old_amount * .2))
            mongo.db.current_month.update_one(user_key, {"$set": {"suggested_savings_amount": suggested_savings}})

        # calculate and send the new amount to the db
        # updated invoice amount in cents
        invoice_amount_cents = euros_to_cents(request.form.get("amount_invoiced"))
         # calculate the amount to set aside for taxes
        invoice_tax_amount = round(new_invoice_tax(invoice_amount_cents, tax_rate))
        # calculate the profit amount
        post_tax_income = round(new_invoice_income(invoice_amount_cents, tax_rate))
        # create a new invoice object
        to_update = {
             "name": session['user'],
            "date": request.form.get("invoice_date"),
            "invoice_number": request.form.get("invoice_number").lower(),
            "invoice_recipient": request.form.get("invoice_recipient").lower(),
            "amount": invoice_amount_cents,
            "invoice_tax_amount": invoice_tax_amount,
            "post_tax_income": post_tax_income,
            "tax": request.form.get("tax"),
            "comments": request.form.get("comments")
        }
        mongo.db.invoices.update({"_id": ObjectId(invoice_id)}, to_update)
        # get credit, add new income
        if request.form.get("tax") == "on":
            # in the case of taxeable income
            credit = mongo.db.current_month.find_one(user_key)["credit"]
            new_credit = invoice_amount_cents  + credit
            # get tax_to_set_aside and add new tax amount
            tax_to_set =  mongo.db.current_month.find_one(user_key)["tax_to_set_aside"]
            new_tax = tax_to_set + invoice_tax_amount
            # update credit and tax_to_set_aside fields
            mongo.db.current_month.update_one(user_key, {"$set": {"credit": new_credit}})
            mongo.db.current_month.update_one(user_key, {"$set": {"tax_to_set_aside": new_tax}})
            # get income_this_month
            old_income = mongo.db.current_month.find_one(user_key)["income_this_month"]
            new_income = old_income + post_tax_income
            # add to income_this_month
            mongo.db.current_month.update_one(user_key, {"$set": {"income_this_month": new_income}})
            # get suggested_savings_amount
            savings = mongo.db.current_month.find_one(user_key)["suggested_savings_amount"]
            suggested_savings = round(savings + (post_tax_income * .2))
            # add to suggested savings this month
            mongo.db.current_month.update_one(user_key, {"$set": {"suggested_savings_amount": suggested_savings}})
        else:
            # in the case of non-taxeable income
            # get credit, add new income 
            credit = mongo.db.current_month.find_one(user_key)["credit"]
            new_credit = credit + invoice_amount_cents
            mongo.db.current_month.update_one(user_key, {"$set": {"credit": new_credit}})
            # get income_this_month
            old_income = mongo.db.current_month.find_one(user_key)["income_this_month"]
            new_income = old_income + invoice_amount_cents
            # add to income_this_month
            mongo.db.current_month.update_one(user_key, {"$set": {"income_this_month": new_income}})
            # get suggested savings, add suggested savings
            savings = mongo.db.current_month.find_one(user_key)["suggested_savings_amount"]
            suggested_savings = round(savings + (invoice_amount_cents * .2))
            mongo.db.current_month.update_one(user_key, {"$set": {"suggested_savings_amount": suggested_savings}})

        # calculate the users disposable income..
        calculate_disposable_income()
        # and create a record
        create_modified_income_record(to_update)
        # provide some feedback
        flash("Invoice successfully updated!")
        return redirect(url_for('invoice'))
    invoice_to_edit = mongo.db.invoices.find_one({"_id": ObjectId(invoice_id)})   
    return render_template("edit_invoice.html", invoice=invoice_to_edit)


@app.route("/delete_invoice/<invoice_id>", methods=["GET", "POST"])
@ensure_user
def delete_invoice(invoice_id):
    if request.method == "POST":
        # set tax rate 
        tax_rate = session["tax_rate"]
        # recalculate credit and relevant fields before updating
        # get credit, income_this_month, suggested_savings_amount, tax_to_set_aside
        user_key = {"name": session['user']}
        current_month = mongo.db.current_month.find_one(user_key)
        credit_before = current_month["credit"]
        income_before = current_month["income_this_month"]
        suggested_savings_before = current_month["suggested_savings_amount"]
        tax_before = current_month["tax_to_set_aside"]
        # get old invoice amount
        old_invoice = mongo.db.invoices.find_one({"_id": ObjectId(invoice_id)})
        old_amount = old_invoice["amount"]
        # set variables for following conditional
        # calculate the amount previously set aside for taxes
        invoice_tax_amount = round(new_invoice_tax(old_amount, tax_rate))
        # calculate the profit amount
        post_tax_income = round(new_invoice_income(old_amount, tax_rate))
        # check whether the invoice was taxeable, recalculate all factors
        if old_invoice['tax'] == "on":
            # in the case of taxeable income
            credit = mongo.db.current_month.find_one(user_key)["credit"]
            new_credit = credit - old_amount
            # get tax_to_set_aside and add new tax amount
            tax_to_set =  mongo.db.current_month.find_one(user_key)["tax_to_set_aside"]
            new_tax = tax_to_set - invoice_tax_amount
            # update credit and tax_to_set_aside fields
            mongo.db.current_month.update_one(user_key, {"$set": {"credit": new_credit}})
            mongo.db.current_month.update_one(user_key, {"$set": {"tax_to_set_aside": new_tax}})
            # get income_this_month
            old_income = mongo.db.current_month.find_one(user_key)["income_this_month"]
            new_income = old_income - post_tax_income
            # update income_this_month
            mongo.db.current_month.update_one(user_key, {"$set": {"income_this_month": new_income}})
            # get suggested_savings_amount
            savings = mongo.db.current_month.find_one(user_key)["suggested_savings_amount"]
            suggested_savings = round(savings - (post_tax_income * .2))
            # add to suggested savings this month
            mongo.db.current_month.update_one(user_key, {"$set": {"suggested_savings_amount": suggested_savings}})
        else:
            # in the case of non-taxeable income
            # get credit, subtract old income 
            credit = mongo.db.current_month.find_one(user_key)["credit"]
            new_credit = credit - old_amount
            mongo.db.current_month.update_one(user_key, {"$set": {"credit": new_credit}})
            # get income_this_month
            old_income = mongo.db.current_month.find_one(user_key)["income_this_month"]
            new_income = old_income - old_amount
            # add to income_this_month
            mongo.db.current_month.update_one(user_key, {"$set": {"income_this_month": new_income}})
            # get suggested savings, add suggested savings
            savings = mongo.db.current_month.find_one(user_key)["suggested_savings_amount"]
            suggested_savings = round(savings - (old_amount * .2))
            mongo.db.current_month.update_one(user_key, {"$set": {"suggested_savings_amount": suggested_savings}})

        # get invoice to delete
        invoice_to_delete = mongo.db.invoices.find_one({"_id": ObjectId(invoice_id)})
        # create a record while its still there, sans credit
        create_deleted_income_record_part_one(invoice_to_delete)
        # delete it
        mongo.db.invoices.remove(invoice_to_delete)
        # get credit after and update the new income record with it
        create_deleted_income_record_part_two()
        # calculate disposable income
        calculate_disposable_income()
        flash("Invoice Deleted!")
        return redirect(url_for('invoice'))

    return redirect(url_for('invoice'))


@app.route("/expenses")
@ensure_user
def expenses():
    expenses = mongo.db.expenses.find({"name": session['user']})
    return render_template("expenses.html", expenses=expenses)


@app.route("/add_expense", methods=["GET", "POST"])
@ensure_user
def add_expense():
    # create reusable user_key
    user_key = {"name": session['user']}
    if request.method == "POST":
        # transform the amount into cents
        amount_to_cents = euros_to_cents(request.form.get("amount_spent"))   
        # create an expense object to send to the db
        new_expense = {
            "name": session['user'],
            "date": request.form.get("invoice_date"),
            "type": request.form.get("type"),
            "recipient": request.form.get('recipient'),
            "amount": amount_to_cents,
            "comments": request.form.get("comments")
        }
        # insert expense object into db
        mongo.db.expenses.insert_one(new_expense)
        # deprecate credit to reflect expenditure
        # get credit
        credit = mongo.db.current_month.find_one(user_key)["credit"]
        new_credit = credit - amount_to_cents
        # update db accordingly
        mongo.db.current_month.update_one(user_key, {"$set": {"credit": new_credit}})
        # get spent_this_month and add new expense 
        total_spent = mongo.db.current_month.find_one(user_key)["spent_this_month"]
        new_total = total_spent + amount_to_cents
        # update db accordingly
        mongo.db.current_month.update_one(user_key, {"$set": {"spent_this_month": new_total}})

        if request.form.get("type") == "Overheads":
            # get overheads_to_be_paid 
            overheads_to_be_paid = mongo.db.current_month.find_one(user_key)["overheads_to_be_paid"]
            # and subtract the amount spent
            new_overheads = overheads_to_be_paid - amount_to_cents
            # get spent_on_overheads
            old_spent_on_overheads = mongo.db.current_month.find_one(user_key)["spent_on_overheads"]
            # add the amount spent
            new_spent_on_overheads = old_spent_on_overheads + amount_to_cents
            # and update the database accordingly
            mongo.db.current_month.update_one(user_key, {"$set": {"overheads_to_be_paid": new_overheads}})
            mongo.db.current_month.update_one(user_key, {"$set": {"spent_on_overheads": new_spent_on_overheads}})
        else:
            # get spent_on_extras
            old_spent_on_extras = mongo.db.current_month.find_one(user_key)["spent_on_extras"]
            # add the amount spent
            new_spent_on_extras = old_spent_on_extras + amount_to_cents
            # and update the database accordingly
            mongo.db.current_month.update_one(user_key, {"$set": {"spent_on_extras": new_spent_on_extras}})

        # calculate the users disposable income...
        calculate_disposable_income()   
        # and create a record
        create_expense_record(new_expense)
        flash("Expense Added!")
        return redirect(url_for('expenses'))
    return render_template("add_expense.html")


@app.route("/edit_expense/<expense_id>", methods=["GET", "POST"])
@ensure_user
def edit_expense(expense_id):
    if request.method == "POST":
        # to recalculate finances so that updated amounts modify rather than add to
        # get original expense amount, credit and add back in

        user_key = {"name": session['user']}
        old_expense = mongo.db.expenses.find_one({"_id": ObjectId(expense_id)})
        old_expense_amount = mongo.db.expenses.find_one({"_id": ObjectId(expense_id)})["amount"]
        credit_before = mongo.db.current_month.find_one(user_key)["credit"]
        credit_to_refactor = old_expense_amount + credit_before
        # update the database temporarily
        mongo.db.current_month.update_one(user_key, {"$set": {"credit": credit_to_refactor}})

        # get spent_this_month and subtract old expense

        total_spent = mongo.db.current_month.find_one(user_key)["spent_this_month"]
        new_total = total_spent - old_expense_amount
        # update db accordingly
        mongo.db.current_month.update_one(user_key, {"$set": {"spent_this_month": new_total}})

        if old_expense["type"] == "Overheads":
            # get overheads_to_be_paid 
            overheads_to_be_paid = mongo.db.current_month.find_one(user_key)["overheads_to_be_paid"]
            # and add the amount back in
            new_overheads = overheads_to_be_paid + old_expense_amount
            # get spent_on_overheads
            old_spent_on_overheads = mongo.db.current_month.find_one(user_key)["spent_on_overheads"]
            # subtract the amount spent
            new_spent_on_overheads = old_spent_on_overheads - old_expense_amount
            # and update the database accordingly
            mongo.db.current_month.update_one(user_key, {"$set": {"overheads_to_be_paid": new_overheads}})
            mongo.db.current_month.update_one(user_key, {"$set": {"spent_on_overheads": new_spent_on_overheads}})
        else:
            # get spent_on_extras
            old_spent_on_extras = mongo.db.current_month.find_one(user_key)["spent_on_extras"]
            # subtract the amount spent
            new_spent_on_extras = old_spent_on_extras - old_expense_amount
            # and update the database accordingly
            mongo.db.current_month.update_one(user_key, {"$set": {"spent_on_extras": new_spent_on_extras}})


        # process the edited document
        amount_to_cents = euros_to_cents(request.form.get("amount_spent"))
        edited_expense = {
            "name": session['user'],
            "date": request.form.get("invoice_date"),
            "type": request.form.get("type"),
            "recipient": request.form.get('recipient'),
            "amount": amount_to_cents,
            "comments": request.form.get("comments")
        }
        mongo.db.expenses.update({"_id": ObjectId(expense_id)}, edited_expense)

        # get credit
        credit = mongo.db.current_month.find_one(user_key)["credit"]
        new_credit = credit - amount_to_cents
        # update db accordingly
        mongo.db.current_month.update_one(user_key, {"$set": {"credit": new_credit}})
        # get spent_this_month and add new expense 
        total_spent = mongo.db.current_month.find_one(user_key)["spent_this_month"]
        new_total = total_spent + amount_to_cents
        # update db accordingly
        mongo.db.current_month.update_one(user_key, {"$set": {"spent_this_month": new_total}})

        if request.form.get("type") == "Overheads":
            # get overheads_to_be_paid 
            overheads_to_be_paid = mongo.db.current_month.find_one(user_key)["overheads_to_be_paid"]
            # and subtract the amount spent
            new_overheads = overheads_to_be_paid - amount_to_cents
            # get spent_on_overheads
            old_spent_on_overheads = mongo.db.current_month.find_one(user_key)["spent_on_overheads"]
            # add the amount spent
            new_spent_on_overheads = old_spent_on_overheads + amount_to_cents
            # and update the database accordingly
            mongo.db.current_month.update_one(user_key, {"$set": {"overheads_to_be_paid": new_overheads}})
            mongo.db.current_month.update_one(user_key, {"$set": {"spent_on_overheads": new_spent_on_overheads}})
        else:
            # get spent_on_extras
            old_spent_on_extras = mongo.db.current_month.find_one(user_key)["spent_on_extras"]
            # add the amount spent
            new_spent_on_extras = old_spent_on_extras + amount_to_cents
            # and update the database accordingly
            mongo.db.current_month.update_one(user_key, {"$set": {"spent_on_extras": new_spent_on_extras}})

        # calculate users disposable income
        calculate_disposable_income()
        # create a record
        create_expense_record(edited_expense)
        # give some user feedback
        flash("Expense Edited Successfully!")
        expenses = mongo.db.expenses.find(user_key)
        return render_template("expenses.html", expenses=expenses)

    expense_to_edit = mongo.db.expenses.find_one({"_id": ObjectId(expense_id)})
    return render_template("edit_expense.html", expense=expense_to_edit)


@app.route("/delete_expense/<expense_id>", methods=["GET", "POST"])
@ensure_user
def delete_expense(expense_id):
        # refactor amount back into credit and update the relevant fields
        # to recalculate finances so that updated amounts modify rather than add to
        # get original expense amount, credit and add back in

        user_key = {"name": session['user']}
        old_expense = mongo.db.expenses.find_one({"_id": ObjectId(expense_id)})
        old_expense_amount = mongo.db.expenses.find_one({"_id": ObjectId(expense_id)})["amount"]
        credit_before = mongo.db.current_month.find_one(user_key)["credit"]
        credit_to_refactor = old_expense_amount + credit_before
        # update the database temporarily
        mongo.db.current_month.update_one(user_key, {"$set": {"credit": credit_to_refactor}})

        # get spent_this_month and subtract old expense

        total_spent = mongo.db.current_month.find_one(user_key)["spent_this_month"]
        new_total = total_spent - old_expense_amount
        # update db accordingly
        mongo.db.current_month.update_one(user_key, {"$set": {"spent_this_month": new_total}})

        if old_expense["type"] == "Overheads":
            # get overheads_to_be_paid 
            overheads_to_be_paid = mongo.db.current_month.find_one(user_key)["overheads_to_be_paid"]
            # and add the amount back in
            new_overheads = overheads_to_be_paid + old_expense_amount
            # get spent_on_overheads
            old_spent_on_overheads = mongo.db.current_month.find_one(user_key)["spent_on_overheads"]
            # subtract the amount spent
            new_spent_on_overheads = old_spent_on_overheads - old_expense_amount
            # and update the database accordingly
            mongo.db.current_month.update_one(user_key, {"$set": {"overheads_to_be_paid": new_overheads}})
            mongo.db.current_month.update_one(user_key, {"$set": {"spent_on_overheads": new_spent_on_overheads}})
        else:
            # get spent_on_extras
            old_spent_on_extras = mongo.db.current_month.find_one(user_key)["spent_on_extras"]
            # subtract the amount spent
            new_spent_on_extras = old_spent_on_extras - old_expense_amount
            # and update the database accordingly
            mongo.db.current_month.update_one(user_key, {"$set": {"spent_on_extras": new_spent_on_extras}})

        # get expense to delete
        expense_to_delete = mongo.db.expenses.find_one({"_id": ObjectId(expense_id)})
        # create a record sans credit after
        create_deleted_expense_record_part_one(expense_to_delete)
        # delete the expense
        mongo.db.expenses.remove(expense_to_delete)
        # update the record object with the updated credit
        create_deleted_expense_record_part_two()
        # calculate disposable income
        calculate_disposable_income()
        flash("Expense Successfully Deleted!")
        return redirect(url_for('expenses'))

@app.route("/user_history")
@ensure_user
def user_history():
    history = mongo.db.in_out_history.find({"name":session['user']})
    return render_template("user_history.html", history=history, name = session['user'])


@app.route("/deductibles", methods=["GET", "POST"])
@ensure_user
def deductibles():
    if request.method == "POST":
        # get session tax rate cookie
        tax_rate = session['tax_rate']
        total_with_tax = float(request.form.get("calculator"))
        tax_to_deduct = new_invoice_tax(total_with_tax, tax_rate)
        return render_template("deductibles.html", tax=tax_to_deduct)
    return render_template("deductibles.html")


@app.route("/wishlist", methods=["GET","POST"])
@ensure_user
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
@ensure_user
def delete_wish(wish):
    if request.method == "POST":
        wish_to_delete = mongo.db.wishlist.find_one({"_id": ObjectId(wish)})
        mongo.db.wishlist.remove(wish_to_delete)
        flash("Wish deleted!")
        return redirect(url_for('wishlist'))
    else: 
        return redirect(url_for('wishlist'))


@app.route("/edit_wish/<wish>", methods=["GET", "POST"])
@ensure_user
def edit_wish(wish):
    if request.method == "POST":
        wish_to_edit = mongo.db.wishlist.find_one({"_id": ObjectId(wish)})
        return render_template("edit_wish.html", wish=wish_to_edit)
    else: 
        return redirect(url_for('wishlist'))


@app.route("/reward", methods=["GET", "POST"])
@ensure_user
def reward():   
    user_reward = mongo.db.rewards.find_one({"name": session['user']})
    return render_template("reward.html", user_reward=user_reward)


@app.route("/image/<filename>")
@ensure_user
def image(filename):
    return mongo.send_file(filename)


@app.route("/add_reward", methods=["GET", "POST"])
@ensure_user
def add_reward():
    if request.method == "POST" and "image" in request.files:
        img = request.files['image']
        to_post = {
        "name": session['user'],
        "img": img.filename,       
        "caption": request.form.get("caption")
        }
        mongo.db.rewards.remove({"name": session['user']})
        mongo.db.fs.files.remove({"name": session['user']})
        mongo.db.fs.chunks.remove({"name": session['user']})
        mongo.save_file(img.filename, img)
        mongo.db.rewards.insert_one(to_post)
        mongo.db.fs.files.update_one({"filename": img.filename}, {"$set": {"name": session['user']}})
        image_key = mongo.db.fs.files.find_one({"filename": img.filename})['_id']
        mongo.db.fs.chunks.update_one({"files_id": image_key}, {"$set": {"name": session['user']} })
        flash("Reward successfully added!")
        return redirect(url_for('reward'))
    return render_template("add_reward.html")

@app.route("/logout")
@ensure_user
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for('login'))


@app.route("/settings")
@ensure_user
def settings():
    # get the current overheads to display on the template for user reference
    current_month = mongo.db.current_month.find_one({"name": session['user']})
    current_overheads = current_month['user_overheads']
    return render_template("settings.html", user=session["user"], current_overheads=current_overheads)


@app.route("/change_overheads", methods=["GET", "POST"])
@ensure_user
def change_overheads():
    # allows the user to change their monthly overheads
    # accessed from the settings page
    # set the user_key to session user
    user_key = {"name": session['user']}
    if request.method == "POST":
        # access the form data
        new_overheads = request.form.get("new_overheads")
        # convert to cents
        new_overheads_to_send = euros_to_cents(new_overheads)
        # access the old overheads for the "to be paid" calculation
        old_overheads = mongo.db.current_month.find_one(user_key)['user_overheads']
        # get spent_on_overheads
        spent_on_overheads = mongo.db.current_month.find_one({"name": session['user']})['spent_on_overheads']
        # create new_overheads_to_be_paid using the new_overheads
        new_overheads_to_be_paid = new_overheads_to_send - spent_on_overheads
        # send it to the db
        mongo.db.current_month.update_one(user_key, {"$set": {"user_overheads": new_overheads_to_send}})
        
        # update overheads_to_be_paid
        mongo.db.current_month.update_one(user_key, {"$set": {"overheads_to_be_paid": new_overheads_to_be_paid}})
        # recalculate the users disposable income
        calculate_disposable_income()
        # give some feedback
        flash("Overheads Successfully Updated!")
        # stay on the same page
        return redirect(url_for('settings'))
    
    return redirect(url_for('settings'))

@app.route("/change_tax_rate", methods=["GET", "POST"])
@ensure_user
def change_tax_rate():
    if request.method == "POST":
        # check to see if a tax rate is selected
        if request.form.get("new_tax_rate") == '':
            # if not, default to Netherlands standard
            tax_rate_to_int = 121            
        else:
            # if so, change the amount to match the user requested, making sure its in the useable format for our functions
            tax_rate_to_string = "1" + str(request.form.get("new_tax_rate"))
            tax_rate_to_int = int(tax_rate_to_string)
        # update the db with the new amount...
        mongo.db.current_month.update_one({"name": session['user']}, {"$set": {"tax_rate": tax_rate_to_int}})
        # and adapt the session cookie to match
        session['tax_rate'] = tax_rate_to_int
        # provide some user feedback
        flash("Tax Rate Updated!")
        # reload the same "settings" page
        return redirect(url_for('settings'))

    return redirect(url_for('settings'))


@app.route("/change_theme", methods=["GET", "POST"])
@ensure_user
def change_theme():
    if request.method == "POST":
        if session['theme'] == "dark":
            mongo.db.current_month.update_one({"name": session['user']}, {"$set": {"preferred_theme": "light"}})
            session['theme'] = "light"
        else:
            mongo.db.current_month.update_one({"name": session['user']}, {"$set": {"preferred_theme": "dark"}})
            session['theme'] = "dark"
        flash("Theme settings updated!")
        return redirect(url_for('settings'))
    return redirect(url_for('settings'))


@app.route("/delete_account")
@ensure_user
def delete_account():
    user_key = {"name": session['user']}
    mongo.db.users.remove(user_key)
    mongo.db.current_month.remove(user_key)
    mongo.db.invoices.remove(user_key)
    mongo.db.expenses.remove(user_key)
    mongo.db.rewards.remove(user_key)
    mongo.db.wishlist.remove(user_key)
    mongo.db.fs.files.remove(user_key)
    mongo.db.fs.chunks.remove(user_key)
    mongo.db.in_out_history.remove(user_key)
    session.clear()
    flash("May Allah enrich all your days. Your account has been deleted.")
    return redirect('login')


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5500")),
        debug=True
    )
