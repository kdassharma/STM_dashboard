import json

import requests
from google.transit import gtfs_realtime_pb2
import time

incomingBuses = []


class IncomingBus:
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

    def getJsonSerialisedBus(self):
        """Turns an IncomingBus object into a json string so it can be requested and parsed in JavaScript"""
        return json.dumps(self.__dict__, indent=2)

    def extractCoordinates(self, vehicle_position):
        """Obtains the latitude and longitude of a bus if it exists in the vehicle_position update"""
        for bus in vehicle_position.entity:
            if self.tripId == bus.vehicle.trip.trip_id:
                return [bus.vehicle.position.latitude, bus.vehicle.position.longitude]


def sortIncomingBuses():
    # sorts all buses based on their IDs and ETAs
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

    return sortedBuses


def extractIncomingBuses(trip_update, vehicle_position):
    relevantBusesWithStops = {'70': '55959', '177': '55871', '213': '55959', '225': '55871'}
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
                        incomingBuses.append(IncomingBus(vehicle_position, stop.stop_id, stop.departure.time, busNumber,
                                                         bus.trip_update.trip.trip_id))


def getIncomingBuses():
    """**Contacts the STM API and processes the received data into a sorted dict of buses inbound to Ericsson**

    ***This is the function that the flask app should call! This refreshes the incomingBuses dict and outputs it!***

    :returns: A dict which contains all the buses headed to Ericsson, the main keys are bus numbers.The attached values are sorted lists of the buses with an identical number.
    :rtype: dict
    """
    global incomingBuses
    # Calling the STM API to request for bus location information and bus stop location
    feed_trip_update = gtfs_realtime_pb2.FeedMessage()
    feed_vehicle_position = gtfs_realtime_pb2.FeedMessage()
    url_trip_updates = "https://api.stm.info/pub/od/gtfs-rt/ic/v1/tripUpdates"
    url_vehicle_position = "https://api.stm.info/pub/od/gtfs-rt/ic/v1/vehiclePositions"

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

    for busNumber in sortedBuses:
        for index, bus in enumerate(sortedBuses[busNumber]):
            sortedBuses[busNumber][index] = bus.getJsonSerialisedBus()

    return sortedBuses

