What is it?
-----------
URLShortener is a URL shortener similar to http://bit.ly, but
with a different URL encoding scheme. The shortened URLs will have the form http://
myurlshortener.com/<word>/ where <word> is a word from the English language.

Installation
-----------
Before running URLShortener you have to install Django. Assuming you have Python and pip
installed, all you have to do is run the following command:

pip install django==1.8a1

The version 1.8 was chosen because of an annoying bug in the previous versions
(https://code.djangoproject.com/ticket/22114), which was fixed in 1.8 only.
After installing Django you have to move yourself to the UrlShortener
directory (the one where this README file is placed). Now you have two options.
You can either load the data from file to the database, or use the existing database.
If you want to use the existing database, just rename sqlite.db_ to sqlite.db

mv sqlite.db_ sqlite.db

Now you can run the URLShortener

python manage.py runserver 

After running this command, you can navigate to http://localhost:8000/.
The URLShortner is up and running. If you are familiar with Django, you may
want to check the admin page - it can be found at http://localhost:8000/-----
That's because the default "http://localhost:8000/admin" can be a valid 
shortened URL.
Login is fyndiq, password is fyndiq.

If you don't want to use the existing database but instead load the words
by yourself, you should first create the tables:

python manage.py syncdb

Now you can run the command to load the words from wordlist to database:

python manage.py load_words words_small.txt

or

python manage.py load_words words.txt -v 2

In the latter case I recommend you to enable verbose output ("-v 2"), because
words.txt contains more than 25000 words and the loading process can take a lot of
time. With verbose output you will know, which word is processed at the moment
and roughly estimate how much time you still need. 

After loading the words, you can run the URLShortener:

python manage.py runserver

Testing
-----------
URLShortener has some tests. To run them, issue the following command:

python manage.py test main initial_loading

Contacts
-----------
If you have any questions, just e-mail pgrafov@gmail.com.
