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

show1 = False # entire vehicle_position list
show2 = False  # entire trip_update list
show3 = False # first entry in vehicle_position
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


