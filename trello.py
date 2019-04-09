import time, json

from flask import request
from flask_restful import Resource

from commands import handler
from dotenv import load_dotenv
load_dotenv()

import os
import requests

class Card():
    def __init__(self, rd):
        t_object = json.loads(
            rd.decode('utf-8')
        )
        self.b_id = t_object["model"]["id"]
        self.action_type = t_object["action"]["type"]
        self.c_name = None
        self.c_id = None
        self.l_name = None
        self.l_id = None
        self.params = []
        if self.action_type == "createCard":
            self.c_name = t_object["action"]["data"]["card"]["name"]
            self.c_id = t_object["action"]["data"]["card"]["id"]
            self.l_name = t_object["action"]["data"]["list"]["name"]
            self.l_id = t_object["action"]["data"]["list"]["id"]
            self.params = self.c_name[1:-1].split(";")

    def destory(self):
        requests.delete(
            f"https://api.trello.com/1/cards/{self.c_id}",
            params = {
                "key": os.getenv("API_KEY"),
                "token": os.getenv("API_TOKEN")
            }
        )

class trello(Resource):
    def post(self):
        action = Card(request.data)
        if action.c_name == None or len(action.params) == 0:
            return "", 204
        if not action.c_name.startswith(">"):
            return "", 204

        handler(action)
        return "", 204

    def head(self):
        return "", 200
