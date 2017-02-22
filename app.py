import sqlite3
import json
from flask import Flask, jsonify, g, request

DATABASE = 'movies.db'

app = Flask(__name__)


def dict_factory(cursor, row):
    """
    :param cursor:
    :type cursor:
    :param row:
    :type row:
    :return: a row formatted as a dictionary based on the cursor and row from the params
    :rtype: dict

    This function takes the standard format of a sqlite3 output and converts it
    into a dictionary row by row.
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d



def get_db():
    """
    :return: returns an open connection to a sqlite3 database
    :rtype: sqlite3.Connection

    A function that opens a connection to the sqlite database and assigns our custom row_factory.
    """
    db = getattr(g, '_database', None)
    if db is None:
        connection = sqlite3.connect(DATABASE)
        connection.row_factory = dict_factory
        db = g._database = connection
    return db


@app.teardown_appcontext
def close_connection(exception):
    """
    :param exception:
    :type exception:

    When the app is closing it makes sure to close the database
    as well using the teardown_appcontext decorator
    """
    db = getattr(g, '_database', None)
    # If there is a database open we want to close it
    if db is not None:
        db.close()


@app.route('/movies/api/v1.0/get_movies', methods=['GET'])
def get_movies():
    """
    :return: get data of all movies in the database
    :rtype: json

    When a client calls the url in the route decorator
    we return all the data in the movies table in a json format.
    """
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
    """
    :return: Requested movie
    :rtype: json

    When a client calls the url in the route decorator with a json containing the key value title
    we return the information associated with that title in the movies table.

    Improvements: We could create a better search function to retrieve the data.
                  as of right now we need an absolute match to return data.
    """
    # Open database and create a cursor
    cur = get_db().cursor()
    # Execute query with the title based on request data from the post request
    # Making sure we use the sqlite3 sql injection protection to protect from malicious attacks
    cur.execute('select * from movies where movie_title = ? order by movie_title',
                (json.loads(request.data)['title'],))
    # Get the results from the executed query in a dictionary
    res = cur.fetchone()
    # Create json out of the dictionary and return it to the api
    return jsonify({'movie': res})

if __name__ == "__main__":
    app.run(debug=True)
