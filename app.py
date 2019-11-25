from flask import Flask
from flask_restful import Api, Resource, reqparse
from testrun_IOTChallenge import *

app = Flask(__name__)
api = Api(app)

buses = incomingBuses


class Bus(Resource):
    def get(self, number):
        for obj in buses:
            if number == obj.busNumber:
                return bus, 200
        return "User not found", 404

    #def post(self, name):

    #def put(self, name):

    #def delete(self, name):


api.add_resource(Bus, "/bus/<string:name>")

app.run(debug=True)