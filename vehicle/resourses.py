from flask import request
from flask_restful import Resource, \
    Api, \
    reqparse, \
    fields, \
    marshal_with, \
    abort

from app import app
from app import db
from .models import Vehicle
from utils import get_object_or_abort, \
    is_user_in_fleet, get_paginated_list

api = Api(app, prefix='/api/vehicles')


post_parser = reqparse.RequestParser()
post_parser.add_argument(
    'name',
    dest='name',
    required=True,
    type=str,
    help='The vehicle\'s name',
)
post_parser.add_argument(
    'fleet_id',
    dest='fleet_id',
    required=True,
    type=int,
    help='The fleet\'s id',
)
post_parser.add_argument(
    'user_id',
    dest='user_id',
    required=False,
    type=int,
    help='The user\'s id',
)

vehicle_fields = {
    'id': fields.Integer,
    'serial_number': fields.String,
    'name': fields.String,
    'fleet_id': fields.Integer,
    'user_id': fields.Integer
}

vehicles_fields = {
    'count': fields.Integer,
    'previous': fields.String,
    'next': fields.String,
    'results': fields.Nested({
        **vehicle_fields
    })
}


class VehiclesResource(Resource):

    @marshal_with(vehicles_fields)
    def get(self):
        fleet_id = request.args.get('fleet_id')
        if fleet_id and fleet_id.isdigit():
            vehicles = Vehicle.query.filter(Vehicle.fleet_id == fleet_id)
        else:
            vehicles = Vehicle.query

        response = get_paginated_list(request, vehicles, per_page=1)
        return response, 200

    @marshal_with(vehicle_fields)
    def post(self):
        args = post_parser.parse_args()

        if args.user_id and \
                not is_user_in_fleet(args.fleet_id, args.user_id):
            return abort(400, message={"user_id": "User must be an employee of Fleet"})

        vehicle = Vehicle(**args)
        db.session.add(vehicle)
        db.session.commit()

        return vehicle, 201


api.add_resource(VehiclesResource, '/')


class VehicleResource(Resource):

    @marshal_with(vehicle_fields)
    def get(self, vehicle_id):
        user = get_object_or_abort(Vehicle, vehicle_id)
        return user, 200

    @marshal_with(vehicle_fields)
    def put(self, vehicle_id):
        vehicle = get_object_or_abort(Vehicle, vehicle_id)

        args = post_parser.parse_args()

        if args.user_id and \
                not is_user_in_fleet(args.fleet_id, args.user_id):
            return abort(400, message={"user_id": "User must be an employee of Fleet"})

        for field, val in args.items():
            setattr(vehicle, field, val)

        db.session.add(vehicle)
        db.session.commit()

        return vehicle, 200

    def delete(self, vehicle_id):
        user = get_object_or_abort(Vehicle, vehicle_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204


api.add_resource(VehicleResource, '/<int:vehicle_id>/')
