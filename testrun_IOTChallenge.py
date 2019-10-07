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
for bus in feed_trip_update.entity:
    if bus.trip_update.trip.route_id == '213':
        print("Bus 213 is here")
        bus.trip_update.trip.route_id
    if bus.trip_update.trip.route_id == '70':
        print("Bus 70 is here")
    if bus.trip_update.trip.route_id == '177':
        print("Bus 177 is here")
    if bus.trip_update.trip.route_id == '177':
        print("Bus 177 is here")
    if bus.trip_update.trip.route_id == '225':
        print("Bus 225 is here")


print(len(feed_trip_update.entity))
print(len(feed_vehicle_position.entity))

bus_vehicle_position = feed_vehicle_position.entity[0]
bus_trip_update = feed_trip_update.entity[0]
bus_number = bus_trip_update.trip_update.trip.route_id
time_stamp = time.ctime(bus_trip_update.trip_update.timestamp)
bus_gps_location = bus_vehicle_position.vehicle.position

