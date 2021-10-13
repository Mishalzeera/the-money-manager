def euros_to_cents(euros_float):
    # takes in a string of euros, * 100 and returns an int of cents
    to_float = float(euros_float)
    return int(to_float * 100)


def cents_to_euros(cents_int):
    # takes in an int of cents, / 100 and returns a float of euros
    return cents_int / 100


def new_invoice_income(invoice_amount):
    # takes in an amount and returns what the user can spend
    tax = invoice_amount - invoice_amount/1.21
    total = invoice_amount - tax
    return total


def new_invoice_tax(invoice_amount):
    # takes in an amount and returns what the user should save for taxes
    tax = invoice_amount - invoice_amount/1.21
    return tax


def overheads_to_be_paid(user_overheads, spent_on_overheads):
    # takes amounts in cents from the db, subtracts the overheads paid from the fixed user given amount
    # no need to convert the currency to euros, since the result goes directly back to db
    to_be_paid = user_overheads - spent_on_overheads
    return to_be_paid

def sum_list(list):
    # takes a list of numbers and returns a total
    total = 0
    for item in list:
        total += item
    return total

