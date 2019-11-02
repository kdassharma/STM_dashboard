import requests
from google.transit import gtfs_realtime_pb2
import time
from datetime import datetime

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


lowest_wait_times = [2147483647, 2147483647, 2147483647]


# ETA algo. 
for bus in feed_trip_update.entity:
    if bus.trip_update.trip.route_id == '70':
        for stop in bus.trip_update.stop_time_update:
            if stop.stop_id == "55788" and int(stop.arrival.time) > 0:
                tempTime = stop.arrival.time
                if tempTime < lowest_wait_times[0]:
                    lowest_wait_times[0] = tempTime
                    
    if bus.trip_update.trip.route_id == '177':
        for stop in bus.trip_update.stop_time_update:
            if stop.stop_id == "55871" and int(stop.arrival.time) > 0:
                tempTime = stop.arrival.time
                if tempTime < lowest_wait_times[1]:
                    lowest_wait_times[1] = tempTime

    if bus.trip_update.trip.route_id == '213':
        for stop in bus.trip_update.stop_time_update:
            if stop.stop_id == "52610" and int(stop.arrival.time) > 0:
                tempTime = stop.arrival.time
                if tempTime < lowest_wait_times[2]:
                    lowest_wait_times[2] = tempTime 


expectedArrival = lowest_wait_times[0] #change index for specific bus
currentTime = int(time.time())
seconds = expectedArrival - currentTime
minutes = seconds/60
expectedArrival = datetime.utcfromtimestamp(expectedArrival).strftime('%Y-%m-%d %H:%M:%S')
print("Expected arrival for bus 70 in UTC: {}".format(expectedArrival))
print("ETA: {} seconds".format(seconds))
print("ETA: {:.1f} minutes".format(minutes))



