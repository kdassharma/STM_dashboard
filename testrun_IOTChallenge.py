import requests
from google.transit import gtfs_realtime_pb2
import time
from datetime import datetime
import math
import sys

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

# Change the following to True/False in order to print /or not print

show1 = False  # entire vehicle_position list
show2 = False  # entire trip_update list
show3 = False  # first entry in vehicle_position
show4 = False  # first entry in trip_update
show5 = False  # all route_ids in vehicle positions
show6 = False  # all route_ids in trip updates

if show1:
    print(feed_vehicle_position)

if show2:
    print(feed_trip_update)

if show3:
    print(feed_vehicle_position.entity[0])

if show4:
    print(feed_trip_update.entity[0])

if show5:
    for bus in feed_vehicle_position.entity:
        print(bus.vehicle.trip.route_id)

if show6:
    for bus in feed_trip_update.entity:
        print(bus.trip_update.trip.route_id)

relevantBuses = {'70': '55788', '177': '55871', '213': '55959'}


# 70 -> 55788, 177 -> 55871, 213 -> 55959
# Function which finds the lowest wait time of a given bus at a given bus stop,
# and then uses the trip_id of that to print its location.
def estimated_time_of_arrival_and_location():
    lowest_wait_time = 99999999999999999999999999999
    lowest_trip_ID = ""

    # busNumber = str(busNumber)
    # stopID = str(stopID)

    # Goes through all bus' stop information and finds the one which goes to requested stopID, and finds the lowest wait time from all of these.
    for bus in feed_trip_update.entity:
        for busNumber in (busNumber for busNumber in relevantBuses if bus.trip_update.trip.route_id == busNumber):
            print(busNumber)
            for stop in bus.trip_update.stop_time_update:
                if stop.stop_id == relevantBuses[busNumber]:
                    tempTime = stop.departure.time
                    if tempTime < lowest_wait_time:
                        lowest_wait_time = tempTime
                        lowest_trip_ID = bus.trip_update.trip.trip_id  # Stores the trip ID of that specific bus with the lowest wait time

    print("Expected arrival in unix time is: {}".format(lowest_wait_time))
    expectedArrival = lowest_wait_time
    currentTime = int(time.time())
    seconds = expectedArrival - currentTime
    minutes = seconds / 60
    expectedArrival = datetime.utcfromtimestamp(expectedArrival).strftime(
        '%Y-%m-%d %H:%M:%S')  # Needs to be changed into local time
    print("Expected arrival for bus {} in UTC: {}".format(busNumber, expectedArrival))
    print("ETA: {} seconds".format(seconds))
    print("ETA: {:.1f} minutes".format(minutes))

    actual_shortest_distance = 99999999999999999999999999999
    busIndex = 0
    count = 0

    for bus in feed_vehicle_position.entity:

        if bus.vehicle.trip.trip_id == lowest_trip_ID:
            print("Trip ID is Valid")
            busIndex = count
        count = count + 1

    print("Bus number 70 is at x-coord: {}".format(feed_vehicle_position.entity[busIndex].vehicle.position.latitude))
    print("Bus number 70 is at y-coord: {}".format(feed_vehicle_position.entity[busIndex].vehicle.position.longitude))

estimated_time_of_arrival_and_location()