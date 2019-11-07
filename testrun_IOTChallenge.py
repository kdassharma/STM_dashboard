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

# Function which finds the lowest wait time of a given bus at a given bus stop, and then uses the trip_id of that to print its location.
def estimated_time_of_arrival_and_location(busNumber, stopID):
    lowest_wait_time = 2147483647 # Will have to fix in year 2038 
    lowest_trip_ID = "" 
    currentTime = int(time.time())
    stop_sequence = 0
    # Goes through all bus' stop information and finds the one which goes to requested stopID, and finds the lowest wait time from all of these. 
    for bus in feed_trip_update.entity:
        if bus.trip_update.trip.route_id == str(busNumber):
            for stop in bus.trip_update.stop_time_update:
                if stop.stop_id == str(stopID):
                    tempTime = int(stop.departure.time)
                    if tempTime < lowest_wait_time and tempTime - currentTime >= 0:
                        stop_sequence = int(stop.stop_sequence) # Stores the stop sequence corresponding to the bus stop entered for later comparision
                        lowest_wait_time = tempTime
                        lowest_trip_ID = str(bus.trip_update.trip.trip_id) # Stores the trip ID of that specific bus with the lowest wait time
    
    if lowest_wait_time == 2147483647: # This is if a bus is not active, it quits out of the function
        return 
    
    print("Expected arrival in unix time is: {}".format(lowest_wait_time))
    expectedArrival = lowest_wait_time 
    seconds = expectedArrival - currentTime
    minutes = seconds/60
    expectedArrival = datetime.utcfromtimestamp(expectedArrival).strftime('%Y-%m-%d %H:%M:%S') # Needs to be changed into local time
    print("Expected arrival for bus {} in UTC: {}".format(busNumber,expectedArrival))
    print("ETA: {} seconds".format(seconds))
    print("ETA: {:.1f} minutes".format(minutes))
    
    tripFound = False
    busIndex = 0
    count = 0
    for bus in feed_vehicle_position.entity:

        if bus.vehicle.trip.trip_id == lowest_trip_ID:
            print("Trip ID was found")
            busIndex = count   
            tripFound = True 
            break
        count=count+1 
    
    if tripFound:
        print("Bus number {} is at (x,y): ({},{})".format(busNumber,feed_vehicle_position.entity[busIndex].vehicle.position.latitude,feed_vehicle_position.entity[busIndex].vehicle.position.longitude))
    else:
        actual_shortest_distance_between_stops = 100
        busIndex = 0
        count = 0
        for bus in feed_vehicle_position.entity:
            if bus.vehicle.trip.route_id == str(busNumber):
                temp_shortest_distance_between_stops = stop_sequence - int(bus.vehicle.current_stop_sequence)
                if temp_shortest_distance_between_stops >= 0 and temp_shortest_distance_between_stops<actual_shortest_distance_between_stops:
                    actual_shortest_distance_between_stops = temp_shortest_distance_between_stops
                    busIndex = count
            count=count+1
        print("Bus number {} is at (x,y): ({},{})".format(busNumber,feed_vehicle_position.entity[busIndex].vehicle.position.latitude,feed_vehicle_position.entity[busIndex].vehicle.position.longitude))

# TESTS:    
estimated_time_of_arrival_and_location("70","55959")
print("--------------------------------------------")
estimated_time_of_arrival_and_location("213","55959")
print("--------------------------------------------")
estimated_time_of_arrival_and_location("177","55871")
