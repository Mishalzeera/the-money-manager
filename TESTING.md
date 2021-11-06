# Testing "Munificent"

## General

A whole slew of issues connecting to the Mongo DB at first. The issue has yet
to be resolved and seems to have affected a lot of people. By switching from 
VS Code to Gitpod, the author was able to continue working.

Deployment to Heroku was successful, however the author had accidentally 
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
the author trying to convert the data in the backend. It was found to be much
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
send bad datatypes to the database as well and bypass required fields. The
author then wrote defensive backend code that checked if any characteristics
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

At the point that the app was a bit more presentable, the author shared it 
with trusted friends. Some have design backgrounds, others in finance as well
as other entrepreneurs. Right away there were some errors that came up due to
their specific way of entering numbers, for instance. Also in their way of 
using the wishlist and rewards functionality. 

Other than backend and technical hiccups, they also brought some UX issues to
the table. Some wanted to be able to navigate easily to another page, while
others thought that some of the colours weren't present enough. 

Of all the testing methodologies, that was among the most useful. The author 
is not familiar with real testing methods, and the short glimpse from the 
Django introduction was enough to make him realise there is a lot more to be
done with testing than previously thought.


