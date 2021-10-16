Do the complex data page first.
Don't forget debug=true

Add mathematic functionality
Streamline the function purpose

- Overheads to be paid 
- Calculate Finances 
- Add Light Mode switch


ENDMONTH FUNCTION ()=> {

1. New Money-month object, "CREDIT", "OVERHEADS TO BE PAID", "WISHLIST", "REWARD
   MEDIA" stay the same, everything else resets to zero

2. Old Money-month object gets pushed to an array.
3. Invoices and expenses pushed to arrays

Style ideas:

Light and dark theme
Cross between tiki and Apple IIc

Munificent

Sheikh Salmans Most Beneficial And Excellent Money Manager 

In this degenerating age, the people are suffering from plague, poverty and oppression. 

The Sheikh, moved by his compassion, has indicated to create Munificent, 
this most excellent, beneficial app that keeps the beloved User in mindful awareness of 
their financial state. 


Add Invoice/Income = 
                     <!-- radio button for calculate tax
                     if "yes"" seperate tax and income, income adds to "credit", tax adds to "tax_to_"
                     if "no" total adds to "credit"
                     send a total combined figure to its own field  -->
                     in_out_history

Add Expense = 
              <!-- if type overhead, subtracts from overheads to be paid (make sure overheads to be paid starts at monthly overheads)
              if type extras, adds to "spent_on_extras" 
              also deprecate Credit! -->
              in_out_history

Edit Invoice/Income = when user clicks on modify button, it stores the total combined in a session cookie, whether taxed or not also
                      when user modifies the amount, session cookie if tax (calculates tax vs income) subtracts the old income from "credit"
                      subtracts the tax amount for "tax_to.." otherwise subtracts total from "credit"
                      then adds the new amount, like in Add Invoice, checking if tax etc

Edit Expense = 
               <!-- when user clicks on the "modify" button, it stores the original expense in a session cookie, whether overhead or not in session cooke
               when user submits the edit, session cookie amount adds to "credit" first, adds to "overheads_to_pay" -->
               <!-- next the new expense is subtracted from credit -->
               in_out_history

In_Out_History =   
                  Create a template page that shows a list of transactions in and out, latest at the top. Matching database. 
                  
                     -date has to be a realtime date of submission independent of any user input.
                     -amount added is a total, includes invoice num if applicable
                     -amount spent includes type and recipient if applicable, 
                     -credit afterwards

In out history page
4MODIFY INCOME
5MODIFY EXPENSE
6DELETE EXPENSE
7DELETE INCOME
Decorator



