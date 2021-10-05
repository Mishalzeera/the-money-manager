Do the complex data page first.
Don't forget debug=true

"CREDIT" - all financial assets, user initialised
"INCOME THIS MONTH" - from previous "NEW INVOICES" or can be added manually
"NEW INVOICE" - calculates tax and adds pretax amount to CREDIT, INCOME THIS
MONTH, adds tax to "AMOUNT TO SET ASIDE"

"SPENT THIS MONTH" - all outgoing
"SPENT ON OVERHEADS" - user-managed sum with annotation
"SPENT ON EXTRAS" - user-managed sum

"OVERHEADS TO BE PAID" - a user-managed sum that is used by the app
"DISPOSABLE INCOME" - all credit minus "SPENT THIS MONTH" and "OVERHEADS TO BE
PAID"
"AMOUNT TO SET ASIDE FOR TAX"
"SUGGESTED SAVINGS AMOUNT"

"WISHLIST" - contains a list of wanted items, cost and whether or not there is
enough "DISPOSABLE INCOME"
"REWARD MEDIA" - when the user presses a button a picture shows

ENDMONTH FUNCTION ()=> {

1. New Money-month object, "CREDIT", "OVERHEADS TO BE PAID", "WISHLIST", "REWARD
   MEDIA" stay the same, everything else resets to zero

2. Old Money-month object gets pushed to an array.

}

Data structure:

U_S_E_R:

-id
-name
-password

C_U_R_R_E_N_T:

-id
-user
-Monthname

P_R_E_V_I_O_U_S:

-id
-user
-first_month
-last_month

Style ideas:

Light and dark theme
Cross between tiki and Apple IIc
