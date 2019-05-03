from flask import request
from flask_restful import Resource, \
    Api, \
    reqparse, \
    fields, \
    marshal_with, \
    abort
from sqlalchemy.exc import IntegrityError

from app import app
from app import db
from utils import get_object_or_abort, \
    get_unique_regex_from_error, get_paginated_list
from .models import Fleet


api = Api(app, prefix='/api/fleets')

post_parser = reqparse.RequestParser()
post_parser.add_argument(
    'name', dest='name',
    required=True,
    type=str,
    help='The fleet\'s name',
)

fleet_fields = {
    'id': fields.Integer,
    'name': fields.String
}

fleets_fields = {
    'count': fields.Integer,
    'previous': fields.String,
    'next': fields.String,
    'results': fields.Nested({
        **fleet_fields
    })
}


class FleetsResource(Resource):

    @marshal_with(fleets_fields)
    def get(self):
        return get_paginated_list(request, Fleet.query, per_page=5)

    @marshal_with(fleet_fields)
    def post(self):
        args = post_parser.parse_args()

        try:
            fleet = Fleet(**args)
            db.session.add(fleet)
            db.session.commit()
        except IntegrityError as e:
            unique_regex = get_unique_regex_from_error(str(e.orig))
            if unique_regex:
                abort(400, message={"name": "Object with this name already exist"})
            else:
                raise
        else:
            return fleet, 201


api.add_resource(FleetsResource, '/')


class FleetResource(Resource):

    @marshal_with(fleet_fields)
    def get(self, fleet_id):
        fleet = get_object_or_abort(Fleet, fleet_id)
        return fleet, 200

    @marshal_with(fleet_fields)
    def put(self, fleet_id):
        fleet = get_object_or_abort(Fleet, fleet_id)

        args = post_parser.parse_args()

        try:
            fleet.name = args.name

            db.session.add(fleet)
            db.session.commit()
        except IntegrityError as e:
            unique_regex = get_unique_regex_from_error(str(e.orig))
            if unique_regex:
                abort(400, message={"name": "Object with this name already exist"})
            else:
                raise
        else:
            return fleet, 200

    def delete(self, fleet_id):
        fleet = get_object_or_abort(Fleet, fleet_id)
        db.session.delete(fleet)
        db.session.commit()
        return '', 204


api.add_resource(FleetResource, '/<int:fleet_id>/')
