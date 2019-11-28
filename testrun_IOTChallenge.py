import json

import requests
from google.transit import gtfs_realtime_pb2
import time
#from datetime import datetime
#import math

relevantBuses = {'70': None, '177': None, '213': None}
relevantBusesWithStops = {'70': '55959', '177': '55871', '213': '55959'}
incomingBuses = []


class incomingBus:
    def __init__(self, vehicle_position, stopId, departureTime, busNumber, tripId):
        self.stopId = stopId
        self.departureTime = departureTime
        self.busNumber = busNumber
        self.tripId = tripId
        # self.utcETA = datetime.utcfromtimestamp(self.departureTime).strftime('%Y-%m-%d %H:%M:%S')
        self.ETA = (self.departureTime - int(time.time())) / 60
        if vehicle_position is not None:
            self.coordinates = self.extractCoordinates(vehicle_position)
        else:
            self.coordinates = vehicle_position

    def getJsonSerialisableBus(self):
        return json.dumps(self.__dict__, indent=2)

    def extractCoordinates(self, vehicle_position):
        for bus in vehicle_position.entity:
            if self.tripId == bus.vehicle.trip.trip_id or str(int(bus.vehicle.trip.trip_id) - 1):
                return [bus.vehicle.position.latitude, bus.vehicle.position.longitude]


def sortIncomingBuses():
    # sorts all buses based on their IDs and ETAs
    lowest_wait_time = 2147483647
    # organising buses by ID
    sortedBuses = {}
    for bus in incomingBuses:
        if bus.busNumber in sortedBuses.keys():
            for index, insertedBus in enumerate(sortedBuses[bus.busNumber]):
                if bus.ETA < insertedBus.ETA:
                    sortedBuses[bus.busNumber].insert(index, bus)
                    break
                elif index == len(sortedBuses[bus.busNumber]) - 1:
                    sortedBuses[bus.busNumber].append(bus)
                    break
            # the loop will never exit if you don't break, as inserting increases the length of the list
        else:
            sortedBuses.update({bus.busNumber: [bus]})
    # # creating a dictionary which contains {busNumber: earliest time for that bus number}
    # for busNum in relevantBuses:
    #     sortedBuses.update({busNum: incomingBus(None, None, lowest_wait_time, None, None)})
    # # the earliest bus objects will be put in dictionary of form {busNum: earliest bus object}
    # for bus in incomingBuses:
    #     if int(bus.departureTime) < sortedBuses[bus.busNumber].departureTime:
    #         sortedBuses[bus.busNumber] = bus
    # # mark all the retained buses as earliest
    # for busNum in sortedBuses:
    #     sortedBuses[busNum].isEarliest = True

    return sortedBuses


def extractIncomingBuses(trip_update, vehicle_position):
    # 70 -> 55788, 177 -> 55871, 213 -> 55959
    global incomingBuses
    incomingBuses = []

    # Goes through all bus' stop information and finds the buses which go to requested stopID, and have yet to reach it.
    for bus in trip_update.entity:
        for busNumber in \
                (busNumber for busNumber in relevantBusesWithStops if bus.trip_update.trip.route_id == busNumber):
            for stop in bus.trip_update.stop_time_update:
                if stop.stop_id == relevantBusesWithStops[busNumber]:
                    # checking if the bus has yet to come to Ericsson
                    if int(time.time()) - int(stop.departure.time) <= 0:
                        incomingBuses.append(incomingBus(vehicle_position, stop.stop_id, stop.departure.time, busNumber,
                                                         bus.trip_update.trip.trip_id))


def getIncomingBuses():
    global incomingBuses
    json_incomingBuses = []
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

    extractIncomingBuses(feed_trip_update, feed_vehicle_position)
    sortedBuses = sortIncomingBuses()

    # for bus in feed_vehicle_position.entity:
    #     if bus.vehicle.trip.trip_id == "204983829":
    #         print("{},{}".format(bus.vehicle.position.latitude, bus.vehicle.position.longitude))
    #
    # for bus in incomingBuses:
    #     print("Bus Number: " + bus.busNumber)
    #     print("Bus ETA: " + str(bus.ETA))
    #     print("coordinates: {},{}".format(bus.coordinates[0], bus.coordinates[1]))
    #     print("=================")
    print(sortedBuses)
    for busNumber in sortedBuses:
        for index, bus in enumerate(sortedBuses[busNumber]):
            sortedBuses[busNumber][index] = bus.getJsonSerialisableBus()

    return sortedBuses

