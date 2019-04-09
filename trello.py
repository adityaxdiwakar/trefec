import time, json

from flask import Flask, request
from flask_restful import Api, Resource, reqparse

class Card():
    def __init__(self, rd):
        t_object = json.loads(
            rd.decode('utf-8')
        )
        self.action_type = t_object["action"]["type"]
        self.c_name = t_object["action"]["data"]["card"]["name"]
        self.c_id = t_object["action"]["data"]["card"]["id"]
        self.l_name = t_object["action"]["data"]["list"]["name"]
        self.l_id = t_object["action"]["data"]["list"]["id"]
        self.params = self.c_name.split(";")[:-1]

class trello(Resource):
    def post(self):
        test = Card(request.data)
        print(test.params)
        json.dump(
            json.loads(request.data.decode('utf-8')),
            open("test.json", "w"),
            indent = 4
        )
        return "", 200

    def head(self):
        return "", 200
