from flask import *
from flask_cors import CORS
from server import controller
import json
import os

app = Flask(__name__)
CORS(app)


@app.route("/search", methods=[ "POST"])
def search():
    form = request.json

    return controller.scrapeSites(form['location'], form['topic'])


if __name__ == "__main__":
  app.run()