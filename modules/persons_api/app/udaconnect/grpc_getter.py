import os
import grpc
from app.location_pb2 import Request
from app.location_pb2_grpc import LocationServiceStub

"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""

print("Sending sample payload...")

GRPC_PORT = os.environ.get("GPRC_PORT", 5005)
GRPC_HOST = os.environ.get("GRPC_HOST", "grpc-api")
# channel = grpc.insecure_channel("host.docker.internal:5008")
channel = grpc.insecure_channel(f"{GRPC_HOST}:{GRPC_PORT}")

stub = LocationServiceStub(channel)

class GrpcClient:
    @staticmethod
    def get_location_list(person_id, start_date, end_date, meters):
        request = Request(
            person_id=int(person_id),
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d"),
            meters=int(meters),
            # person_id = 6,
            # start_date = "2020-01-01",
            # end_date = "2020-12-30",
            # meters = 500
        )
        response = stub.Get(request)

        return response.locations
