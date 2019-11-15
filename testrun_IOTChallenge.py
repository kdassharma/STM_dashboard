import requests
from google.transit import gtfs_realtime_pb2
import time
from datetime import datetime
import math
import sys


class incomingBus:
    def __init__(self, bus, stopId, departureTime, busNumber, tripId):
        self.bus = bus
        self.stopId = stopId
        self.departureTime = departureTime
        self.busNumber = busNumber
        self.tripId = tripId
        # self.utcETA = datetime.utcfromtimestamp(self.departureTime).strftime('%Y-%m-%d %H:%M:%S')
        self.ETA = (self.departureTime - int(time.time())) / 60
        self.coordinates = self.extractCoordinates()
        self.isEarliest = False

    def extractCoordinates(self):
        for bus in feed_vehicle_position.entity:
            if self.tripId == bus.vehicle.trip.trip_id or str(int(bus.vehicle.trip.trip_id) - 1):
                return [bus.vehicle.position.latitude, bus.vehicle.position.longitude]


# Calling the STM API to request for bus location information and bus stop location
feed_trip_update = gtfs_realtime_pb2.FeedMessage()
feed_vehicle_position = gtfs_realtime_pb2.FeedMessage()
url_trip_updates = "https://api.stm.info/pub/od/gtfs-rt/ic/v1/tripUpdates"
url_vehicle_position = "https://api.stm.info/pub/od/gtfs-rt/ic/v1/vehiclePositions"
payload = ""

headers = {
    'origin': "mon.domain.xyz",
    'apikey': "l7xxfec365f2dad04b158e1583f6fc4a23cf"
}

response_trip_update = requests.request("POST", url_trip_updates, headers=headers)
response_vehicle_Positions = requests.request("POST", url_vehicle_position, headers=headers)
feed_trip_update.ParseFromString(response_trip_update.content)
feed_vehicle_position.ParseFromString(response_vehicle_Positions.content)

relevantBuses = {'70': None, '177': None, '213': None}
relevantBusesWithStops = {'70': '55788', '177': '55871', '213': '55959'}
incomingBuses = []


def markEarliestBuses():
    lowest_wait_time = 2147483647
    earliestBuses = {}
    # creating a dictionary which contains {busNumber: earliest time for that bus number}
    for busNum in relevantBuses:
        earliestBuses.update({busNum: incomingBus(None, None, lowest_wait_time, None, None)})
    # the earliest bus objects will be put in dictionary of form {busNum: earliest bus object}
    for bus in incomingBuses:
        if int(bus.departureTime) < earliestBuses[bus.busNumber].departureTime:
            earliestBuses[bus.busNumber] = bus
    # mark all the retained buses as earliest
    for busNum in earliestBuses:
        earliestBuses[busNum].isEarliest = True
    # return earliestBuses for possible debugging
    return earliestBuses


def estimated_time_of_arrival_and_location():
    # 70 -> 55788, 177 -> 55871, 213 -> 55959
    global incomingBuses
    incomingBuses = []

    # Goes through all bus' stop information and finds the buses which go to requested stopID, and have yet to reach it.
    for bus in feed_trip_update.entity:
        for busNumber in \
                (busNumber for busNumber in relevantBusesWithStops if bus.trip_update.trip.route_id == busNumber):
            for stop in bus.trip_update.stop_time_update:
                if stop.stop_id == relevantBusesWithStops[busNumber]:
                    # checking if the bus has yet to come to Ericsson
                    if int(time.time()) - int(stop.departure.time) <= 0:
                        incomingBuses.append(incomingBus(bus, stop.stop_id, stop.departure.time, busNumber,
                                                         bus.trip_update.trip.trip_id))


estimated_time_of_arrival_and_location()
earliestBuses = markEarliestBuses()

for bus in incomingBuses:
    print("Bus Number: " + bus.busNumber)
    print("Bus ETA: " + str(bus.ETA))
    print("isEarliest?: " + str(bus.isEarliest))
    print("=================")