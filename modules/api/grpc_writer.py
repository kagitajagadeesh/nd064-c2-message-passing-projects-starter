import os
import sys
import time
import grpc
from concurrent import futures
from datetime import datetime, timedelta


from app.grpc_api import location_pb2
from app.grpc_api import location_pb2_grpc
from app.grpc_api.location_pb2 import LocationMessage

from app import db
from app.udaconnect.models import Location

from wsgi import app


class LocationServicer(location_pb2_grpc.LocationServiceServicer):
    def Get(self, request, context):
        start_date = datetime.strptime(request.start_date, "%Y-%m-%d")
        end_date = datetime.strptime(request.end_date, "%Y-%m-%d")
        person_id = request.person_id
        meters = request.meters
        # first_order = order_pb2.OrderMessage(
        #     id="2222",
        #     created_by="USER123",
        #     status=order_pb2.OrderMessage.Status.QUEUED,
        #     created_at='2020-03-12',
        #     equipment=[order_pb2.OrderMessage.Equipment.KEYBOARD]
        # )

        # second_order = order_pb2.OrderMessage(
        #     id="3333",
        #     created_by="USER123",
        #     status=order_pb2.OrderMessage.Status.QUEUED,
        #     created_at='2020-03-11',
        #     equipment=[order_pb2.OrderMessage.Equipment.MOUSE]
        # )

        data = []
        with app.app_context():
            locations = db.session.query(Location).filter(
                    Location.person_id == person_id
                ).filter(Location.creation_time < end_date).filter(
                    Location.creation_time >= start_date
                ).all()
            print(locations)
            for location in locations:
                data.append(
                    LocationMessage(
                        person_id=location.person_id,
                        longitude=location.longitude,
                        latitude=location.latitude,
                        meters = meters,
                        start_date = datetime.strftime(start_date, "%Y-%m-%d"),
                        end_date= datetime.strftime(end_date, "%Y-%m-%d")
                    )
                )

        result = location_pb2.LocationMessageList(locations=data)
        # result.orders.extend([first_order, second_order])
        return result

    # def Create(self, request, context):
    #     print("Received a message!")

    #     request_value = {
    #         "id": request.id,
    #         "person_id": request.person_id,
    #         "longitude": request.longitude,
    #         "latitude": request.latitude,
    #         "creation_time": request.creation_time,
    #     }
    #     print(request_value)

    #     return location_pb2.LocationMessage(**request_value)


# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
# order_pb2_grpc.add_OrderServiceServicer_to_server(OrderServicer(), server)
location_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), server)


print("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)

# def start_server():
#     if os.environ.get('https_proxy'):
#         del os.environ['https_proxy']
#     if os.environ.get('http_proxy'):
#         del os.environ['http_proxy']

#     port = 5008
#     print(f"Server starting on port {port}")
#     server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
#     server.add_insecure_port(f"0.0.0.0:{port}")
#     server.start()

#     return server


# # Initialize gRPC server

# server_instance = start_server()
# location_servicer = LocationServicer()
# location_pb2_grpc.add_LocationServiceServicer_to_server(location_servicer, server_instance)

# try:
#     while True:
#         time.sleep(86400)
# except KeyboardInterrupt:
#     print("\nGoodbye")
#     server_instance.stop(0)
