import sqlite3
import json
from flask import Flask, jsonify, g, request

DATABASE = 'movies.db'

app = Flask(__name__)


# Create a factory to return dictionary instead of a list
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


# Function to open the database and assign the row type
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        connection = sqlite3.connect(DATABASE)
        connection.row_factory = dict_factory
        db = g._database = connection
    return db

# Close connection when we are done with it
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    # If there is a database open we want to close it
    if db is not None:
        db.close()


@app.route('/movies/api/v1.0/get_movies', methods=['GET'])
def get_movies():
    # Open database and create a cursor
    cur = get_db().cursor()
    # Execute query
    cur.execute('select * from movies')
    # Get the results from the executed query in a dictionary
    res = cur.fetchall()
    # Create json out of the dictionary and return it to the api
    return jsonify({'movies': res})

@app.route('/movies/api/v1.0/get_movie', methods=['POST'])
def get_movie():
    # Open database and create a cursor
    cur = get_db().cursor()
    # Execute query
    cur.execute('select * from movies where movie_title = ? order by movie_title',
                (json.loads(request.data)['show_me_what_you_got'],))
    # Get the results from the executed query in a dictionary
    res = cur.fetchone()
    # Create json out of the dictionary and return it to the api
    return jsonify({'movie': res})

if __name__ == "__main__":
    app.run(debug=True)
