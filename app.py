import flask
from flask import Flask
from flask_restful import Api, Resource, reqparse
import json
import testrun_IOTChallenge as test


def adjustHeaders(response, method):
    """**Takes a response and adds the proper headers along with the given allowed methods.**

    :param response: The generated response that needs to have additional headers.
    :type response: flask Response object
    :param method: The HTTP methods that are allowed to get that response
    :type method: str

    :returns: None
    """
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', method)


class STMBuses(Resource):

    def get(self):
        """**Contacts the backend to obtain the buses with a certain bus number, which it returns as a flask response.**

        Takes an extra HTTP parameter that is parsed with reqparse, which represents the bus number requested.
        The list containing all the buses with that number is obtained by contacting the backend.
        The list is turned into a json string and given to a flask response constructor.
        The proper headers are added to that response.

        :param self: The only available bus resource
        :type self: STMBuses

        :returns: A response that contains the json string representation of the list of buses with a certain bus number
        :rtype: flask response
        """
        identifier = "busId"
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
        """**Contacts the backend to obtain all the buses, returns them as a flask response.**

        The dict containing all the buses is obtained by contacting the backend.
        The dict is turned into a json string and given to a flask response constructor.
        The proper headers are added to that response.

        :param self: The only available bus resource
        :type self: STMBuses

        :returns: A response that contains the json string representation of the dict that contains all buses
        :rtype: flask response
        """
        global buses
        if len(buses) == 0:
            returnCode = 201
        else:
            returnCode = 200
        buses = test.getIncomingBuses()
        response = flask.make_response(json.dumps({"incomingBuses": buses}), returnCode)
        adjustHeaders(response, 'PUT')
        return response

    # this somehow executes along with put, when it's called from js.
    def options(self):
        """**Replies to the OPTIONS request that is always emitted before a PUT/POST request.**

        Creates a response with valid
        The proper headers are added to that response.

        :param self: The only available bus resource
        :type self: STMBuses

        :returns: A response that contains the json string representation of the dict that contains all buses
        :rtype: flask response
        """
        if len(buses) == 0:
            returnCode = 201
        else:
            returnCode = 200
        response = flask.make_response("acknowledged", returnCode)
        adjustHeaders(response, 'OPTIONS,PUT')
        return response


if __name__ == "__main__":
    app = Flask(__name__)
    api = Api(app)

    buses = {}
    displayBuses = STMBuses()

    api.add_resource(STMBuses, "/bus/")

    app.run(debug=True)

