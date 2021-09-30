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
up.
