import flask
from flask import Flask
from flask_restful import Api, Resource, reqparse
import json

import testrun_IOTChallenge as test

app = Flask(__name__)
api = Api(app)

buses = {}
identifier = "busId"


def adjustHeaders(response, method):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', method)


class STMBuses(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument(identifier)
        args = parser.parse_args()
        try:
            response = flask.make_response(json.dumps(buses[args[identifier]]), 200)
        except KeyError:
            response = flask.make_response("null", 404)
        adjustHeaders(response, 'GET')
        return response

    def put(self):
        global buses
        if len(buses) == 0:
            returnCode = 201
        else:
            returnCode = 200
        buses = test.getIncomingBuses()
        response = flask.make_response(json.dumps({"incomingBuses": buses}), returnCode)
        adjustHeaders(response, 'PUT')
        return response

    # this somehow executes instead of put, when it's called from js.
    def options(self):
        # global buses
        if len(buses) == 0:
            returnCode = 201
        else:
            returnCode = 200
        # buses = test.getIncomingBuses()
        # response = flask.make_response(json.dumps(buses), returnCode)
        response = flask.make_response("acknowledged", returnCode)
        adjustHeaders(response, 'OPTIONS,PUT')
        return response


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

