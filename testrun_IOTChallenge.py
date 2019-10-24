import requests
from google.transit import gtfs_realtime_pb2
import time

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


# ETA algo. for one random bus
for bus in feed_trip_update.entity:
    # can replace this with any bus route_id, just need to change stopID to an actual stop_id for that bus
    if bus.trip_update.trip.route_id == '211':
        for stop in bus.trip_update.stop_time_update:
            stopID = "58479"
            if stop.stop_id == stopID:
                print("Bus 211 is here")
                print("{} stop found".format(stopID))
                expectedArrival = stop.arrival.time
                print("Expected arrival in unix time: {}".format(expectedArrival))
                currentTime = int(time.time())
                seconds = expectedArrival - currentTime
                minutes = seconds/60 + (seconds - (seconds/60)*60)%60
                print("ETA: {} seconds".format(seconds))
                print("ETA: {} minutes".format(minutes))

print("length of trip_update list: {}".format(len(feed_trip_update.entity)))
print("length of vehicle_position list: {}".format(len(feed_vehicle_position.entity)))

