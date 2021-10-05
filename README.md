## Notes on the README approach

Previously there was some difficulty with creating a useful README. In earlier
projects, wireframes and other development journaling were omitted to some
degree. In this project the author will attempt to document the process from
start to finish via the README creation process.

This means that no code will be written or any action on the project undertaken
without a README entry being written first. This will lead to a long and
possibly unwieldy document, but it is an approach the author would like to try
in the spirit of learning good methodology. Also, Flask/Python/backend dev in
general seems like it could be helpful to have a trail of trials and eroors.

If it doesn't work out that well, he will return back to flailing around in his
code editor while mismanaging his extensions. He will return to writing his
READMEs at the end of his processes, more to vent frustration than provide
any clear guidance to a future collaborator.

## Order of operations

On the advice of the author's mentor, backend/database functionality should
be implemented first before spending time on styling. In this instance, the
application will be built first and then styled afterwards. The mockups will
therefore be attended to further into the development process.

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
feature may well be implemented in the future, the author felt it would be
beyond the scope of this app. This is due to the possibility of a user who is,
as mentioned in the previous paragraph, on a contract and has a different
setup, financially.

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
is also working fine. However still a persistent error message ("pymongo.errors.ServerSelectionTimeoutError") and no app launch in VSCode.

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





