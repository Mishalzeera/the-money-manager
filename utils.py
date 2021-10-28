def euros_to_cents(euros_float):
    # takes in a string of euros, * 100 and returns an int of cents
    to_float = float(euros_float)
    return int(to_float * 100)


def cents_to_euros(cents_int):
    # takes in an int of cents, / 100 and returns a float of euros
    return cents_int / 100


def new_invoice_income(invoice_amount, tax_rate_int):
    # takes in an amount and returns what the user can spend
    tax = invoice_amount - invoice_amount/(tax_rate_int / 100)
    total = invoice_amount - tax
    return total


def new_invoice_tax(invoice_amount, tax_rate_int):
    # takes in an amount and returns what the user should save for taxes
    tax = invoice_amount - invoice_amount/(tax_rate_int / 100)
    return tax


def overheads_to_be_paid(user_overheads, spent_on_overheads):
    # takes amounts in cents from the db, subtracts the overheads paid from the fixed user given amount
    # no need to convert the currency to euros, since the result goes directly back to db
    to_be_paid = user_overheads - spent_on_overheads
    return to_be_paid


def validate_registration_form(form):
    #takes in the request.form object and applies conditional logic.
    #returns an error list

    #create variables
    name_maxlength = 50
    name_minlength = 4
    password_maxlength = 15
    password_minlength = 5
    error_list = []

    if not form["name"] or len(form["name"]) > 50 or len(form["name"]) < 4:
        error_list.append("Name field cannot be empty, less than 4 or more than 50 characters.")
    

    if not form["password"] or len(form["password"]) > 15 or len(form["password"]) < 5:
        error_list.append("Password field cannot be empty, less than 5 or more than 15 characters.")

    try:
        float(form["starting-credit"])
        if not form["starting-credit"]:
            error_list.append("You must enter a starting credit and it must be a number.")

    except ValueError:
        error_list.append("You must enter a starting credit and it must be a number.")

    try:
        float(form["user-overheads"])
        if not form["user-overheads"]:
            error_list.append("You must enter a starting credit and it must be a number.")

    except ValueError:
        error_list.append("You must enter your monthly overheads and it must be a number.")


    return error_list