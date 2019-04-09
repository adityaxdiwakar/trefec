from flask import Flask
from flask_restful import Api

from trello import trello
import time, json

#initiializing the flask webapp
app = Flask(__name__)
api = Api(app)

#writing trello endpoint
api.add_resource(trello, "/trello")

app.run(host='127.0.0.1', port=1337, debug=True)