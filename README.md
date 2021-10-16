# The Money Manager

An app that will allow a user to keep track of different streams of financial
concern. Expenditure in areas like bills, rent and general overheads,
as well as an income area where invoice details can be entered,
which will then calculate a tax amount to set aside and set into a different
category.

There will be different constant variable sums:

- total credit
- total monthly expenditure
- total monthly income
- total monthly tax to pay
- suggested savings amount

Also a wishlist area that stores links to desired products, and keeps track of
when you have enough extra money that purchasing one of your wishlist products
is viable.

The ideal user is a freelancer who has relatively simple finances and a young
business she is nurturing. While they aren't terrible with money, they may not
be good at keeping track of what their financial standing is.

# Primary Abstract Features

- Freelancers typically experience a "feast or famine" situation and it is
  always advised to keep some capital extra on the side for the "famine" months.
  One of the features of the app is to help the user protect themselves from being
  too comfortable during a "feast" stage and overspending.

- At the moment when an expansion/investment decision is to be made, the user
  has the opportunity to be certain of their situation financially.

- The user can refer to the past months of financial activity and keep track
  of their own pattern, helping them make better decisions overall.

## Practical Features

- A clear, simple user interface that makes daily financial discipline less
  of a chore.

- A general dashboard that gives basic feedback, primarily "Total Credit" and
  "Amount spent this month".

- A more detailed page where the user can see more endpoints, such as "amount
  spent this month on bills", "income from invoices", "pending invoices"

- A reward system that makes using the app a pleasure, such as
  images that remind the user of a financial goal. For example, the user
  may have the wish to earn enough as a freelancer to live in Bali and work from
  a laptop. She can then upload an image of a person on a Balinese beach typing
  on a nice MacBook air.

- An archive of past months finances.

## Limiting the scope of the app

Due to the complex way in which personal finances can work, this app can be
set up for a person on a normal job contract who wishes to keep track of
their expenses and save up for, for example, a new motorbike.

However, the author had the idea to create a corresponding feature which would
push the figures to an Google Spreadsheet to make tax season easier. While the
feature may well be built in the future, the author felt it would be
beyond the scope of this app. This is due to the possibility of a user who is,
as mentioned in the previous paragraph, on a contract and has a different
setup, financially.

## Notes on the README approach

Previously there was some difficulty with creating a useful README. In earlier
projects, wireframes and other development journaling were omitted to some
degree. In this project the author will attempt to document the process from
start to finish via the README creation process.

This means that no code will be written or any action on the project undertaken
without a README entry being written about it. This will lead to a long and
possibly unwieldy document, but it is an approach the author would like to try
in the spirit of learning good methodology. Also, Flask/Python/backend dev in
general seems like it could be helpful to have a trail of trials and eroors.

If it doesn't work out that well, he will return back to flailing around in his
code editor while mismanaging his extensions. He will return to writing his
READMEs at the end of his processes, more to vent frustration than provide
any clear guidance to a future collaborator.

## Order of operations

On the advice of the author's mentor, backend/database functionality should
be done first before spending time on styling. In this instance, the
application will be built first and then styled afterwards. The mockups will
therefore be attended to further into the development process.

# Creating a working platform

### Installing dependencies.

At this moment, from an earlier project it looks like the necessary libraries,
flask, pymongo, dnspython etc are all in place. Using the pip list command in
the terminal, it was ascertained that this was indeed the case. A learning
moment, as it was assumed that the dependencies were installed somewhere in the
project repository files.

### Basic file structures

Since this is a Flask project, the author will create the "templates" and
"static" folders first. Then, "app.py", ".gitignore", "env.py", "Procfile",
then a "requirements.txt", since these are all going to be used.

### Initialising Flask

Setting app = Flask(**name**) first, then running a simple script to ascertain
indeed that Flask is working. Import os and Flask. Env page needed to be set
up. Live server settings updated and the (if name == main) logic initialised.
Flask working.

### Creating Database in Mongo

Switching to Mongo DB to create a new cluster for the project. Some challenge
in mentally organising the data beforehand, but it can always be reorganised.
Mongo, it seems, has moods and is slow this evening. A new project was created
with the name "the-money-manager". The database was named "money_db". Then
"users", "current_month" and "previous_months" collections were added. Also
"wishlist" and "reward".

### Connecting and Testing Mongo to App

Using the same naming convention as the walkthrough exercise, env variables
were set in "env.py" as well as configurated in "app.py".

Some kind of persistent issue with being unable to access Mongo from the
local VSCode environment raised its head at this point. After a few hours of
Stack Overflow and Youtube videos, including modifying URI strings and
reinstalling packages, no connection could be made to Mongo.

Opening the repository in GitPod from the GitHub page and creating a temporary
env file did launch the app fine. So then it was deployed to Heroku, where it
is also working fine. However still a persistent error message 
("pymongo.errors.ServerSelectionTimeoutError") and no app launch in VSCode.

Strangely this is also happening with previous projects that were begun
successfully but scrapped for this current idea.

To keep the project momentum going, it will be written in GitPod. Added some
graphics for further down the road since it is easier to do that in VSCode.


### Create A Base Working Template

In GitPod a new "env.py" file was created. It has been helpful to have to restart
a few times and learn more about the strategic purpose of an env file. Then a
base working template as well as a form structure to register was created.

### Create Registration Functionality

After creating a basic form in HTML and giving it some workeable styling,
there was some need for data-type conversion, so a utility Python file was created
to hold functions that would do all of that. After importing the file at the top
of app.py, functions within the helper page were finetuned to convert the string
value from the the form first to a float, then an integer multiplied by 100. This
gives the value in cents, which is the standard way to store and retrieve currency
data, according to a Youtube film on ecommerce the author had watched. 

In the registration function, the data is split into two streams. One stream is the
new user and password dataset, the other is a "current month" dataset. Within the 
body of the function, the helper functions from "functions.py" were invoked and 
used to provide the cents value for the "insert_one" method.

There were a few issues of syntax which caused the data to arrive in an "array" 
rather than the straighforward integer. This was resolved and the project 
committed and pushed to Github.

### Create Login Functionality

Despite having attempted a few Flask projects, the author found it necessary to 
follow along with the Flask Mini Project 20 and adapt the code moves as necessary. 
Similarly to the project walkthrough, the registration page was adapted. There 
was more indepth research of regex patterns to ensure that the "starting credit"
and "monthly costs" registration fields were correct, so that the database is in
good shape. So there was some going back and forth beteen the login and registration
pages and views. 

### Addressing 302 Error Loops

Passing the same variable back to the view as an argument resulted, invariably, in
endless loops that tied up the server with a 302 error. This was resolved by gaining
a better understanding of how Flask works with passing variables from one scope
enclosure to another. Also with a better understanding of how session cookies work.
After this was handled, it was a lot clearer how to handle the variables sent to the 
templates as well, and some of the nuance of it became apparent.

### Create Logout Functionality

For the time being, the Logout function will simply clear all cookies and redirect to 
the Login page. Index and related views were adapted with the defensive code "if 'user'
not in session:", using the else statement for when the user session cookie is in play.

### Access User Data From Database

The next step is displaying the fields from the database in the profile page. Also blank
buttons that will allow the user to update their finances and view their wishlist/reward.
The data is converted from cents to euros using a helper function. The form settings
for the registration page had to be adjusted with a step="0.01" attribute, which allows
floats to be sent to the database. Before going to the database they are converted in the
app.py function to an integer. 

### Adapt Internal Links

For the sake of keeping things coherent, an if statement was added to base.html, showing
login/register vs logout options depending on the state. The condition of "user" being in
session cookies was used as the deciding factor. Also it is worth noting that around here
the CI walkthrough project was no longer of myuch help and the author stopped using it as
a reference.

### Create Settings Page That Allows User To Delete Account

To avoid the tedious deletion of individual items in the database manually, it was decided
to create a "settings" page where the user can delete the account. Later on its possible 
that more functions will be added, but for now, it helps to keep the process all within
the app itself. 

### Create Wishlist

A Wishlist, accessed via the users profile page, contains a list of items the user would like
to save up for. This is sent to its own collection in the database after a "add wish" form
is filled in. The item appears immediately in the wishlist. Adding a dynamically generated
a-tag with a url_for that links to a route only allows for the routing but not passing any
variables back. Despite combing the Jinja and Flask docs, the author could only find limited
mention of any related information. The issue was resolved by changing the a-tag to a button,
and wrapping in a form tag. 

### Create Invoice Structure

The author has been grappling with the organisation of concerns, and has found that having a
basic HTML and render_template route for a feature in place helps. This allows the flow of
operations to be clear to the author, who has to focus on small tasks, one at a time. The
basic CRUD setup of the invoicing feature may involve separate pages for some functions, but
remain in the same template for others. The invoice structure was set up as a series of pages
for the time being. Once everything was set up and working, there was some grappling with the 
return value of the amount field from the database, which was in cents. Since the invoice page
variable passed to the template was a dictionary of dictionaries, it wasn't clear at first how
to apply the cents_to_euros() function to that one particular value. However, Jinja templating
allows for mathematical operations, and the easiest solution for the time being was to simply
incorporate that into the formatting. {{ invoice.amount /100 }}

### Create A Rewards Page

The idea of the rewards page is to provide a single, ongoing source of inspiration to the user.
It is hoped that during times when the user is tempted to spend their remaining income on something
unnecessary, the reward image and caption will remind them of a greater goal. For the sake of 
simplicity as well as adding a learning outcome - uploading a file - the author will limit the 
reward section to an image and a simple caption.

With the help of a Youtube video "Save and Retrieve Files In MongoDB With Flask + Pymongo" the
author was able to create an image upload/display function. A new method was learned using a 
route as a way to pass data rather than for managing templates. In the template where the image
was to be displayed, within an img tag, the src attribute was given the url_for('display function 
route', filename='variable passed from the page route which uses user session cookies.img'). The
Filename variable passed from this src went to a special route function that called the correct
file from Mongo db, and passed it through to the correct template.

This helped understand the many potentials that working with backend code allows. 

### Adding Expenses Functions

It was realised at this late stage that "Expense" functionality had not been added, despite being
of primary importance to the concept behind the app. In the process of setting it up and connecting
it to the database, much was learned about the difference between GET and POST settings in the form
tag. A recurring error kept the author occupied until the method was changed in the form, since the
request being made was not, in fact, posting any information to the db. 

### All Basic CRUD Functionality In Place

From here on, the next thing to focus on is building up the "functions.py" module so that "app.py" 
can process the data in and out of its way to the front-end. During this process it is expected that
some core functionality of the app may be adapted as the overview becomes clear. At the moment
the author is still unclear on how it would be to use the app in practise, since the author himself
is really the ideal candidate for the role of User. In other words, not the most financially astute. 
Current challenges include the most succinct and adaptable way to process individual value fields 
coming as a BSON object from Mongo. The author will begin with writing the core mathematic functions.

### Streamlining Basic Functionality In Motion

As the app developed, it became clear that the main streams of incoming and outgoing finances had to 
conform to a format. For instance, in the expense form, it was previously a text input that the user
could choose - "rent" "cigars" "whiskey" etc. However, in order to keep the database calculable the
decision to use radio buttons was made. This forces  the user to decide whether the expense is an
"overhead" or an "extra". An additional comment field was added in case greater specificity is
needed. The invoice form was adapted to also reflect income from other sources (cash, off the books,
criminal income) by allowing the user to enter an amount and whichever of the fields wished for. A
series of if statements show only the completed fields in the main "incoming" page. The author can 
now go back to bringing the calculations into play.

### Modifications To Income/Expense Forms

Buttons had to be added to both Income/Expense input forms to ensure that the users finances 
can be dynamically updated correctly upon modification. For instance, if a user enters an invoice for 
a service that is untaxeable, then the user should have control over whether or not the amount is 
processed for tax. The app is opinionated in setting aside the tax amount without including it in 
the total credit, making sure the user doesn't overspend. However, with cash income (being paid back
a loan for instance), having a checkbox that says "do not calculate tax" keeps it efficient.

This also allows for modifying invoice amounts "after the fact". The plan at the moment is, upon the
user selecting to modify a specific invoice, the invoices amount gets stored in a session cookie. Also,
whether or not it was taxeable or not also gets stored in a session cookie. Upon submitting the new 
modified amount, the app will first recalculate the users finances to remove the old invoice amount
correctly regarding tax etc. Then the new amount is processed. 

Similarly, with expenses being checked as of type "overhead" or not, the dynamic recalculation of
expense amounts is now possible. The author is hoping that his understanding of how session cookies
work is correct, in that anything can be assigned as a session variable. 

So far this approach seems overly verbose, and the author is sure that some kind of refactoring of
functions behind the scenes could take place. However, it may be best to do that after all the 
functionality is in place, however naive it may be. It may be simply a matter of managing imports
and modules correctly. Also, there was no need for session cookies, simply writing the verbose but
workable code in the right place did the job. 

One puzzling bug was forgetting to update the object sent back from the edit-invoice to match
the original add invoice schema. It was a big learning moment for the author about the practicalities
of the assingment. There was a persistent key error when trying to reupdate an invoice (past the first
time updating it) since important values (specifically the checkbox that determines whether or not tax
should be calculated) were being replaced with None/Null. The entire invoice object was being erased 
and recreated, this time without the all important checkbox field. It took some time to realise what
was going on.