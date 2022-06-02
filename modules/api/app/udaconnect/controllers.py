from datetime import datetime

from app import producer
from app.udaconnect.models import Connection, Location
from app.udaconnect.schemas import (
    ConnectionSchema,
    LocationSchema,
)
from app.udaconnect.services import ConnectionService, LocationService
from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import Optional, List

DATE_FORMAT = "%Y-%m-%d"
TOPIC_NAME = 'locations'

api = Namespace("UdaConnect", description="Connections via geolocation.")  # noqa


# TODO: This needs better exception handling


@api.route("/locations")
@api.route("/locations/<location_id>")
@api.param("location_id", "Unique ID for a given Location", _in="query")
class LocationResource(Resource):
    @accepts(schema=LocationSchema)
    @responds(schema=LocationSchema)
    def post(self) -> Location:
        producer.send(TOPIC_NAME, request.data)
        # request.get_json()
        # location: Location = LocationService.create(request.get_json())
        return request.get_json();

    @responds(schema=LocationSchema)
    def get(self, location_id) -> Location:
        location: Location = LocationService.retrieve(location_id)
        return location

