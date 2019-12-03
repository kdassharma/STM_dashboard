import flask
from flask import Flask
from flask_restful import Api, Resource, reqparse
import json

import testrun_IOTChallenge as test

app = Flask(__name__)
api = Api(app)

buses = {}
identifier = "busId"


class STMBuses(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument(identifier)
        args = parser.parse_args()
        try:
            response = flask.make_response(buses[args[identifier]], 200)
        except KeyError:
            response = flask.make_response(buses[args[identifier]], 404)
        self.adjustHeaders(response)
        return response

    def put(self):
        global buses
        if len(buses) == 0:
            returnCode = 201
        else:
            returnCode = 200
        buses = test.getIncomingBuses()
        response = flask.make_response(json.dumps(buses), returnCode)
        self.adjustHeaders(response)
        return response

    def adjustHeaders(self, response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST')


displayBuses = STMBuses()


@app.route('/bus/display')
def display():
    return displayBuses.put()


@app.route('/testing', methods=['GET', 'PUT'])
def testing():
    response = flask.jsonify({'some': 'data'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

api.add_resource(STMBuses, "/bus/")

app.run(debug=True)

