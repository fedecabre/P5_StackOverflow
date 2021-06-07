# Code from https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

import flask #Imports the Flask library, making the code available to the rest of the application.
from flask import request, jsonify
import sqlite3

app = flask.Flask(__name__) # Creates the Flask application object, which contains data about the application and also methods (object functions) that tell the application to do certain actions.
app.config["DEBUG"] = True #Starts the debugger. With this line, if your code is malformed, you’ll see an error when you visit your app. Otherwise you’ll only see a generic message such as Bad Gateway in the browser when there’s a problem with your code.

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# Create some test data for our catalog in the form of a list of dictionaries.
books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''

# A route to return all of the available entries in our catalog.
@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory #lets the connection object know to use the dict_factory function we’ve defined, which returns items from the database as dictionaries rather than lists—these work better when we output them to JSON.
    cur = conn.cursor() # the object that actually moves through the database to pull our data
    all_books = cur.execute('SELECT * FROM books;').fetchall() #we execute an SQL query with the cur.execute method to pull out all available data (*) from the books table of our database.

    return jsonify(all_books)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/v1/resources/books', methods=['GET'])
def api_filter():
    query_parameters = request.args
    id = query_parameters.get('id')
    published = query_parameters.get('published')
    author = query_parameters.get('author')
    # The function first grabs all the query parameters provided in the URL (remember, query parameters are the part of the URL that follows the ?, like ?id=10).

    query = "SELECT * FROM books WHERE"
    to_filter = []

    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    # examine the provided URL for an id and select the books that match that id.
    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if published:
        query += ' published=? AND'
        to_filter.append(published)
    if author:
        query += ' author=? AND'
        to_filter.append(author)
    if not (id or published or author):
        return page_not_found(404)

# Data passed through URLs like this (after the ?) are called query parameters. They’re a feature of HTTP used for filtering for specific kinds of data.
    query = query[:-4] + ';' # To perfect our query, we remove the trailing ` AND and cap the query with the ;` required at the end of all SQL statements:

    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)

    # Create an empty list for our results
#    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
#    for book in books:
#        if book['id'] == id:
#            results.append(book)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
#    return jsonify(results)

app.run() # A method that runs the application server.