import os
import grpc
import location_pb2
import location_pb2_grpc

"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""

print("Sending sample payload...")

GRPC_PORT = os.environ.get("GPRC_PORT", 5005)
GRPC_HOST = os.environ.get("GRPC_HOST", "grpc-api")
# channel = grpc.insecure_channel("host.docker.internal:5008")
channel = grpc.insecure_channel(f"{GRPC_HOST}:{GRPC_PORT}")

stub = location_pb2_grpc.LocationServiceStub(channel)

def create_location(person_id, latitude, longitude):
    # request = Request(
    #     person_id=int(person_id),
    #     start_date=start_date.strftime("%Y-%m-%d"),
    #     end_date=end_date.strftime("%Y-%m-%d"),
    #     meters=int(meters),
    #     # person_id = 6,
    #     # start_date = "2020-01-01",
    #     # end_date = "2020-12-30",
    #     # meters = 500
    # )

    # response = stub.Get(request)
    message = location_pb2.LocationMessage(
            person_id,
            latitude,
            longitude
    )
    response = stub.create(message)

    return response

test_location = create_location(1, "37.55363", "-122.290883")
print(test_location)