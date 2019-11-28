import json

from flask import Flask
from flask_restful import Api, Resource, reqparse
import testrun_IOTChallenge as test

app = Flask(__name__)
api = Api(app)

buses = []


class STMBuses(Resource):

    def get(self, busId):
        try:
            return buses[busId], 200
        except KeyError:
            return "Bus not found", 404

    def put(self):
        global buses
        if len(buses) == 0:
            returnCode = 201
        else:
            returnCode = 200
        buses = test.getIncomingBuses()
        return {"incomingBuses": buses}, returnCode


displayBuses = STMBuses()


@app.route('/bus/display')
def display():
    return displayBuses.put()


api.add_resource(STMBuses, "/bus/<string:busId>")

app.run(debug=True)

# # can put back later
# def get(self, number):
#     for obj in buses:
#         if number == obj.busNumber:
#             return bus, 200
#     return "User not found", 404
