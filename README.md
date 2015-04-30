Worktogether - Tell and know what your team is working on
============================================================

* Get a mail everyday asking what did you do today
* Send a mail everyday with your response
* Get a mail next day with everyone's responses.

Inspired by idonethis.com

Technical Details
====================

* Emails are parsed by sendgrid and https://github.com/agiliq/sendgrid-eventhooks
* Django app parses text from email

Data received in receiver function
=======================================

Data is received as a dictionary in kwargs which has two keys 'sender' and 'data'. The 'data' key has the dict of information from 'sendgrid-eventhooks'
The keys in 'data' dict are:
* Sender
* To
* Date
* Subject
* Body

Todo
=====================

* Allow team members to customize the time at which they want to receive the email.
