DATABASE SCHEMATIC FOR MUNIFICENT

money_db (parent database passed to the Pymongo() function)

<!-- The parent database that all the other collections are stored in -->

    -current_month:

<!-- The main current user database that is used for the main dashboard -->

        ---id: {mongo generated}
        ---name: {user defined string}
        ---datestamp: {automatically generated month/year stamp}
        ---credit: {number initially entered by user, dynamically calculated by app}
        ---user_overheads: {number initially entered by user, dynamically calculated by app}
        ---income_this_month: {number dynamically calculated by app}
        ---spent_this_month: {number dynamically calculated by app}
        ---spent_on_overheads: {number dynamically calculated by app}
        ---spent_on_extras: {number dynamically calculated by app}
        ---overheads_to_be_paid: {number dynamically calculated by app}
        ---tax_rate: {set by user}
        ---tax_to_set_aside: {number dynamically calculated by app}
        ---suggested_savings_amount: {number dynamically calculated by app}
        ---disposable_income: {number dynamically calculated by app}
        ---user_notes: {user entered and maintained}
        ---preferred_theme: {initiated by app, modified by user}

    -expenses

<!-- The collection that stores expenses used to calculate key user figures -->

        ---id: {mongo generated}
        ---name: {user defined string}
        ---date: {user defined string}
        ---datestamp: {automatically generate month/year stamp}
        ---type: {selected by user from two options}
        ---recipient: {user defined string}
        ---amount: {number entered by user}
        ---comments: {user defined string}

    -fs.chunks

<!-- A collection created by Mongo that stores the actual image binary code -->

        ---id: {mongo generated}
        ---files-id: {mongo generated, connects to fs.files}
        ---n: {mongo generated}
        ---data: {mongo generated, binary}

    -fs.files

<!-- A collection created by Mongo that stores image-related data -->

        ---id: {mongo generated}
        ---filename: {mongo generated}
        ---contentType: {mongo generated}
        ---md5: {mongo generated}
        ---chunksize: {mongo generated}
        ---length: {mongo generated}
        ---uploadDate: {mongo generated}
        ---name: {added in by the app so that user data can be managed}

    -in_out_history

<!-- A collection of user records displayed on the history.html template -->

        ---id: {mongo generated}
        ---name: {user defined string}
        ---date: {automatically generate month/year stamp}
        ---amount: {number entered by user}
        ---recipent: {user defined string}
        ---tax: {number dynamically calculated by app}
        ---credit_after: {number dynamically calculated by app}
        ---type: {selected by user from two options}


    -invoices

<!--  A collection of income entries with user defined tax Boolean -->

        ---id: {mongo generated}
        ---name: {user defined string}
        ---date: {user defined string}
        ---datestamp: {automatically generate month/year stamp}
        ---invoice_number: {user defined string}
        ---invoice_recipient: {user defined string}
        ---amount: {number entered by user}
        ---invoice_tax_amount: {number dynamically calculated by app}
        ---post_tax_income: {number dynamically calculated by app}
        ---tax: {Boolean whether or not tax calculated for invoice}
        ---comments: {user defined string}

    -previous_months

<!-- A collection of past month records, generated upon login when the month has passed -->

        ---id: {mongo generated}
        ---name: {user defined string}
        ---period: {automatically generate month/year stamp}
        ---spent_this_month: {number dynamically calculated by app}
        ---income_this_month: {number dynamically calculated by app}
        ---spent_on_overheads: {number dynamically calculated by app}
        ---spent_on_extras: {number dynamically calculated by app}
        ---tax_to_set_aside: {number dynamically calculated by app}
        ---ending_credit: {number dynamically calculated by app}

    -rewards

<!-- A collection of images, one per user, for the rewards.html template -->

        ---id: {mongo generated}
        ---name: {user defined string}
        ---img: {image name from file upload}
        ---caption: {user defined string}

    -tax_seasons

<!-- A collection of tax records to display on the history.html template -->

        ---id: {mongo generated}
        ---name: {user defined string}
        ---period_ending: {automatically generate month/year stamp}
        ---tax_rate: {set by user}
        ---tax_to_set_aside: {number dynamically calculated by app}
        ---credit_after: {number dynamically calculated by app}

    -users

<!-- A collection of current users with their hashed passwords -->

        ---id: {mongo generated}
        ---name: {user defined string}
        ---password: {user defined string}

    -wishlist

<!-- A collection of wishlist items with an 'is_affordable' Boolean -->

        ---id: {mongo generated}
        ---name: {user defined string}
        ---wish_name: {user defined string}
        ---wish_cost: {number entered by user}
        ---wish_description: {user defined string}
        ---is_affordable: {Boolean dynamically calculated by app}