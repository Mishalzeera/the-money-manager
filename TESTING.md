# Testing "Munificent"

## General

A whole slew of issues connecting to the Mongo DB at first. The issue has yet
to be resolved and seems to have affected a lot of people. By switching from 
VS Code to Gitpod, I was able to continue working.

Deployment to Heroku was successful, however I had accidentally 
installed something using Node Package Manager, which caused the app not to
run, and only after combing the directory was it noticed that there were all
these Node-related files. Deleting them solved the issue.

A lack of clear understanding regarding variables and scoping when passing to
and from a template caused errors. However these were quickly solved and moved
on from.

## Testing The Database

A tab was opened on the browser which allowed for a quick check of the Mongo 
DB activity. First, testing general connectivity and then testing whether or 
not the app was processing the figures and entries correctly.

This wasn't as straightforwards as it might sound, since there is some issue of
data-type conversion with Mongo. Also the terminology - "doubles" are floats, 
for instance. 

There was simply no other way of testing the correct values and data-types 
other than sending them to a template and trying to get them to render right.
Sometimes the issues were with the intial form settings, and sometimes with 
myself trying to convert the data in the backend. It was found to be much
easier to fix in the templates themselves using Jinja calculation methods.

Introducing media files caused the database to create its own collections to
manage things. This made for some complexity with keeping track of what was
connected to what. Again, the database had to be directly accessed in the 
browser and media erased from within the Mongo database.

Once the database was written with the correct values, it was less of a problem
and things could be tested without having to go back and forth to the database.
A simple "delete account" action would remove the image and all its associated
data.

## Testing The Templates

It is trickier testing HTML templates than it was thought. Commenting out 
Jinja code does not in fact render it invisible to the browser. One has to
manually switch back and forth from the open port to the code base as one 
tries to fix something. 

## Testing And Validating Forms

HTML forms are easy to brute force override, and there was nothing in place to
prevent that. Pressing F12 and erasing HTML attributes made it possible to 
send bad datatypes to the database as well and bypass required fields. I then 
wrote defensive backend code that checked if any characteristics
of an entry violated tthe desired schematic, and if so would not allow the 
relevant functions to work. 

## Testing Buttons

The nature of building an app like this more or less ensures succesful internal
links, since as a matter of course, Jinja/Flask will throw an error otherwise.
However there was some finesse regarding the differences between an "a"tag 
styled as a button and an actual submit button - in terms of instantiating 
form actions. Due to the backend not throwing an error, it was harder to 
diagnose, as it is easy to overlook something so simple when you are new to it.

## Friends 

At the point that the app was a bit more presentable, I shared it 
with trusted friends. Some have design backgrounds, others in finance as well
as other entrepreneurs. Right away there were some errors that came up due to
their specific way of entering numbers, for instance. Also in their way of 
using the wishlist and rewards functionality. 

Other than backend and technical hiccups, they also brought some UX issues to
the table. Some wanted to be able to navigate easily to another page, while
others thought that some of the colours weren't present enough. 

Of all the testing methodologies, that was among the most useful. I 
am not familiar with real testing methods, and the short glimpse from the 
Django introduction was enough to make me realise there is a lot more to be
done with testing than previously thought.

## Lighthouse

At the suggestion of the mentor, Lighthouse was used to check the accessibility 
and general "best practises" of the app. Both light and dark themes got "100" 
for Best Practises, "91" for SEO. Dark theme got "84" for Accessibility, where
light theme got "91". For Performance, dark theme got "91" and light theme got
"84". 

## Validators

W3 Validator for dark_style.css passed with 12 exceptions due to using custom
variables - Validator doesn't include them in its processes. "Due to their
dynamic nature, CSS custom variables are not statically checked". The same
result was had for light_style.css and style.css. tw-colours.css, being only
a sheet of custom variables, needs no validation. 

For the HTML validation, there were a few 'errors' regarding spacing between
attributes, which I quickly fixed and ran again. Also there is a persistent
message that the "pattern attribute does not apply" to the type of input I had
chosen to use. However, it does indeed have the outcome I wanted, so I will
assume that is one of the HTML Validator's quirks. 

--add_expense.html: Validated successfully other than Jinja code

--add_invoice.html: Validated successfully other than Jinja code

--add_reward.html: Validated successfully other than Jinja code

--admin.html: Validated successfully other than Jinja code

--base.html: Validated successfully other than Jinja code

--delete_account.html: Validated successfully other than Jinja code

--delete_expense.html: Validated successfully other than Jinja code

--delete_invoice.html: Validated successfully other than Jinja code

--edit_expense.html: Validated successfully other than Jinja code

--edit_invoice.html: Validated successfully other than Jinja code

--edit_note.html: Validated successfully other than Jinja code

--edit_wish.html: Validated successfully other than Jinja code

--end_tax.thml: Validated successfully other than Jinja code

--expenses.html: Validated successfully other than Jinja code

--index.html: Validated successfully other than Jinja code

--invoice.html: Validated successfully other than Jinja code

--login.html: Validated successfully other than Jinja code

--manual.html: Validated successfully other than Jinja code

--profile.html: Validated successfully other than Jinja code

--register.html: Validated successfully other than Jinja code

--reward.html: Validated successfully other than Jinja code

--settings.html: Validated successfully other than Jinja code

--user_history.html: Validated successfully other than Jinja code

--wishlist.html: Validated successfully other than Jinja code

## Javascript testing

Since the Javascript is very minimal in this app - simply fading pages in as
the user navigates - testing it was as simple as adding an 'alert' to the 
Javascript file and making sure it showed when refreshing the page.

GSAP was used, and placed in the correct order with a very simple custom
script. 

# Suggested Tests For Possible Future Maintainability

| Test Label |Test Action  |Expected Outcome|Test Outcome|
|--|--|--|--|
|Navigate to app  |Enter the base URL |Auto-redirects to '/login' - **Login**|PASS |
|Switch to **Register**|Click either link labelled 'Register'|Switches to the Registration form|PASS|
|Register a new user|Enter details in the registration form|App goes to '/index' - **Quick View**|PASS|
|Navigate to **Dashboard**|Click the logo-icon with the label 'To Dashboard'|App goes to '/profile/username' - **Dashboard**|PASS|
|Toggle **Dashboard** to **Quick View**|Click the same logo-icon now labelled 'To Quick View'|App reverts to **Quick View** and back to **Dashboard**|PASS|
|Create Note|Enter some text in the note-field and click 'Create Note'|New note created, input field changes to note, 'Create Note' button now 'Edit Note'|PASS|
|Navigate to **Edit Note**|Click the 'Edit Note' button|App goes to '/edit_note/' - **Edit Note** page|PASS|
|Test Note Modification|Change the text in the note-field and click 'Modify Note'|Return to **Dashboard** and see modified note.|PASS|
|Navigate to **Invoice/Income** page|Click the 'Invoices/Income' button|App navigates to '/invoice' - **Invoice/Income** page|PASS|
|Navigate to **Add New Invoice/Income**|Click 'Add New Income' button|App navigates to '/add_invoice/...' **Add New Invoice/Income**| PASS |
|Add An Invoice|Fill in the form and click 'Add Invoice'|App navigates back to **Invoice/Income** and the new income is visible|PASS|
|Modify The Invoice|Click the 'Modify' button under the new entry, adapt the entry and click 'Modify'|App navigates back to **Invoice/Income**, tax and income is recalculated in all related fields in **Dashboard**|PASS|
|Delete the Invoice|Click the 'Delete' button under the entry|App navigates to a warning page, upon confirmation the app redirects to the **Invoice/Income** page and all related fields in **Dashboard** reflect the deletion|PASS|
|Navigate to the **Expenses** page|Click the 'Manage Expenses' button in **Dashboard**|App navigates to the **Expenses** page|PASS|
|Add an Expense|Click the 'Add Outgoing Expense' button, fill and submit form|App navigates to the **Add Expense** page, upon submit the app navigates back to **Expenses** and shows the new entry - all related entries updated in **Dashboard**|PASS|
|Modify an Expense|Click 'Modify' under newly created entry, change some fields and submit|App reverts to **Expenses** and shows the updated entry, all related **Dashboard** fields correctly reflect the modification|PASS|
|Delete an Expense|Click 'Delete' under entry, and confirm |Upon confirmation Expense is deleted, all related fields in **Dashboard** reflect the change.|PASS|
|Navigate to **End Your Taxes** page|Click 'End Your Tax Period' in the **Dashboard**|App navigates to '/end_tax' - **End Your Taxes**|PASS|
|Test the Calculator|Enter a total of an amount including tax into the Calculator, submit and check that tax is separated from non-taxed amount|Tax and non-taxed amount appear on the screen in correct proportions determined by the global tax rate|PASS|
|End the Tax Period|Navigate to the '/user_history' **History** page, check that there is no 'Previous Tax Season', navigate back to **End Your Taxes** check the box and click 'End Your Tax Period' - Navigate back to **History** to check|In **History** a new Previous Tax Season shows|PASS|
|Check **History** shows correct data|Use **Expense** and **Invoice/Income** pages to add dummy data, log out and manually change the current month datestamp field in the database (current_month-> datestamp) then log in again. Repeat the **End Your Taxes** test, then navigate to **History**|In the History page, on the left are all the types of in and out activity, the right has a Previous Months entry and a PreviousTax Seasons entry |PASS|
|Navigate to **Wishlist**|From **Dashboard** click the 'Wishlist' link item in the navbar|Navigates to the **Wishlist** page|PASS|
|Test Add Wish|Fill in the form and press 'Add New Wish'|App refreshes the **Wishlist** page and the new Wish appears|PASS|
|Test Modify Wish|Click the 'Edit Wish' button by the new wish, alter the entry, click 'Save Changes' |App returns to the **Wishlist** page showing the updated entry|PASS|
|Test Delete Wish|Click the 'Delete' button by the new Wish|Page refreshes and Wish is deleted|PASS|
|Navigate to **Reward**|From **Dashboard** click the 'Reward' link item in the navbar|Navigates to **Reward**|PASS|
|Test Add Reward|Click on 'Add An Inspiring...' button, fill in and submit the form|**Reward** pages refreshes with added image and caption, button changing to 'Change Your...'|PASS|
|Navigate to **Manual**| From any page in the app, click the 'Manual' link item in the navbar|Navigates to the **Manual**|PASS|
|Navigate to **Settings**|From any page in the app, click the cogs icon in the navbar|Navigates to **Settings**|PASS|
|Test Overheads Update|Making note of the placeholder number in the input field, enter a new overheads figure and click 'Change Your Monthly Overheads'|Page refreshes and placeholder updates to the new amount, check **Dashboard** to be certain|PASS|
|Test Change Tax Rate|Making note of the placeholder percentage, enter a new percentage and click 'Change Your Tax Rate'|Page refreshes and placeholder updates to the new amount, check **Dashboard** to be certain|PASS|
|Test Toggle Light/Dark Theme|Making sure your eyes are open, click on the 'Toggle Theme Light/Dark' button|The appearance switches from dark to light and vice versa|PASS|
|Test Delete Account|Using a temporary fake account, log in to MUNIFICENT, click 'Delete Account' and confirm|Navigates to **Login** and deleted username is no longer recognised|PASS|
|Navigate to **Admin**|Log into Admin account, and click the 'Admin' link item in the navbar|Navigates to **Admin**|PASS|
|Test Delete User|From list of current users, select a particularily offensive user, tick the safety box and click 'Delete User'|User is deleted from the app, including all data, check database|PASS|




















