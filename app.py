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


@app.route("/invoice")
def invoice():
    invoices = mongo.db.invoices.find() 
    return render_template("invoice.html", invoices=invoices)


@app.route("/add_invoice", methods=["GET", "POST"])
def add_invoice():
    if request.method == "POST":
        # convert the currency from euros to cents
        invoice_amount_cents = euros_to_cents(request.form.get("amount_invoiced"))
        # calculate the amount to set aside for taxes
        invoice_tax_amount = round(new_invoice_tax(invoice_amount_cents))
        # calculate the profit amount
        post_tax_income = round(new_invoice_income(invoice_amount_cents))
        # create a new invoice object
        new_invoice = {
            "name": session['user'],
            "date": request.form.get("invoice_date"),
            "invoice_number": request.form.get("invoice_number").lower(),
            "invoice_recipient": request.form.get("invoice_recipient").lower(),
            "amount": invoice_amount_cents,
            "invoice_tax_amount": invoice_tax_amount,
            "post_tax_income": post_tax_income,
            "tax": request.form.get("taxeable"),
            "comments": request.form.get("comments")
        }
        # insert new object
        mongo.db.invoices.insert_one(new_invoice)
        # create reusable key
        user_key = {"name": session['user']}
        # get credit, add new income
        if request.form.get("taxeable") == "on":
            # in the case of taxeable income
            credit = mongo.db.current_month.find_one(user_key)["credit"]
            new_credit = post_tax_income + credit
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

        # provide confirmation to user:
        flash("Invoice successfully added!")
        return redirect(url_for('profile', username=session['user']))

    return render_template("add_invoice.html")


@app.route("/edit_invoice/<invoice_id>", methods=["GET", "POST"])
def edit_invoice(invoice_id):
    if request.method == "POST":
        invoice_amount_cents = euros_to_cents(request.form.get("amount_invoiced"))
        to_update = {
            "name": session['user'],
            "date": request.form.get("invoice_date"),
            "invoice_number": request.form.get("invoice_number").lower(),
            "invoice_recipient": request.form.get("invoice_recipient").lower(),
            "amount": invoice_amount_cents,
            "comments": request.form.get("comments")
        }
        mongo.db.invoices.update({"_id": ObjectId(invoice_id)}, to_update)
        flash("Invoice successfully updated!")
        return redirect(url_for('invoice'))
    invoice_to_edit = mongo.db.invoices.find_one({"_id": ObjectId(invoice_id)})
    
    for key, value in invoice_to_edit.items():
        if key == "amount":
            # update using helper function from functions.py
            invoice_to_edit.update({key: cents_to_euros(value)})
            # send the new dict to the template
                
    
    return render_template("edit_invoice.html", invoice=invoice_to_edit)


@app.route("/delete_invoice/<invoice_id>", methods=["GET", "POST"])
def delete_invoice(invoice_id):
    if request.method == "POST":
        invoice_to_delete = mongo.db.invoices.find_one({"_id": ObjectId(invoice_id)})
        mongo.db.invoices.remove(invoice_to_delete)
        flash("Invoice Deleted!")
        return redirect(url_for('invoice'))

    return redirect(url_for('invoice'))


@app.route("/expenses")
def expenses():
    expenses = mongo.db.expenses.find()
    return render_template("expenses.html", expenses=expenses)


@app.route("/add_expense", methods=["GET", "POST"])
def add_expense():
    if request.method == "POST":
        amount_to_cents = euros_to_cents(request.form.get("amount_spent"))
        new_expense = {
            "name": session['user'],
            "date": request.form.get("invoice_date"),
            "type": request.form.get("type"),
            "recipient": request.form.get('recipient'),
            "amount": amount_to_cents,
            "comments": request.form.get("comments")
        }
        mongo.db.expenses.insert_one(new_expense)
        flash("Expense Added!")
        return redirect(url_for('expenses'))
    return render_template("add_expense.html")


@app.route("/edit_expense/<expense_id>", methods=["GET", "POST"])
def edit_expense(expense_id):
    if request.method == "POST":
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
        flash("Expense Edited Successfully!")
        expenses = mongo.db.expenses.find()
        return render_template("expenses.html", expenses=expenses)

    expense_to_edit = mongo.db.expenses.find_one({"_id": ObjectId(expense_id)})
    return render_template("edit_expense.html", expense=expense_to_edit)


@app.route("/delete_expense/<expense_id>", methods=["GET", "POST"])
def delete_expense(expense_id):
    
        expense_to_delete = mongo.db.expenses.find_one({"_id": ObjectId(expense_id)})
        mongo.db.expenses.remove(expense_to_delete)
        flash("Expense Successfully Deleted!")
        return redirect(url_for('expenses'))


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


@app.route("/reward", methods=["GET", "POST"])
def reward():   
    user_reward = mongo.db.rewards.find_one({"name": session['user']})
    return render_template("reward.html", user_reward=user_reward)


@app.route("/image/<filename>")
def image(filename):
    return mongo.send_file(filename)


@app.route("/add_reward", methods=["GET", "POST"])
def add_reward():
    if request.method == "POST" and "image" in request.files:
        img = request.files['image']
        to_post = {
        "name": session['user'],
        "img": img.filename,       
        "caption": request.form.get("caption")
        }
        
        mongo.save_file(img.filename, img)
        mongo.db.rewards.insert_one(to_post)
        flash("Reward successfully added!")
        return redirect(url_for('reward'))
    return render_template("add_reward.html")

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
    mongo.db.invoices.remove({"name": session["user"]})
    flash("May Allah enrich all your days. Your account has been deleted.")
    session.clear()
    return redirect('login')


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5500")),
        debug=True
    )
