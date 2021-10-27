form validation
login with email
update() instead of multiple update_one()s
db schema
if datestamp on invoices and expenses doesn't match current month, no CRUDding.
delete pages as confirmation
crud ugly squoosh
PEP... 8... COMPLIANT
Don't forget debug=true
history page shows tax seasons and previous months
search feature!
currency titles, maybe always have credit one colour
Round off the figures with the floats tiny nearby
https://themeforest.net/category/site-templates?term=dashboard
https://drive.google.com/drive/u/0/folders/1n2iFWqA44Wlc4GLXCBwN023L-KGAYE2D
Refactor modules
{{number | round | int }}


Creating an endmonth function. When the user registers, a datestamp is created. Whenever the user logs in, the
app checks the date of the datestamp in the db. If the %y %m is not the same, a new datestamp replaces the old 
one and overheads to be paid, suggested savings resets, etc. To show on user history page

Creating an end tax period, user initiated, has a checkbox to ensure that the user is ready to do it. Then
creates a new tax_season object, sending to a separate database, and shown on the user history page. The 
relevant fields reset. 


Style ideas:

Light and dark theme
Cross between tiki and Apple IIc

Munificent

Sheikh Salmans Most Beneficial And Excellent Money Manager 

In this degenerating age, the people are suffering from plague, poverty and oppression. 

The Sheikh, moved by his compassion, has indicated to create Munificent, 
this most excellent, beneficial app that keeps the beloved User in mindful awareness of 
their financial state. 


from app import mongo


