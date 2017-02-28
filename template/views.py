from api_client import Api
from flask import Flask, render_template
import json

app = Flask(__name__)


@app.route('/')
def index():
    api = Api()
    r = json.loads(api.all_movies().text)
    return render_template("index.html", movies=r["movies"])

if __name__ == '__main__':
    app.run(debug=True, port=5000)