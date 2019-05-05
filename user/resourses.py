from flask import request
from flask_restful import Resource, \
    Api, \
    reqparse, \
    abort, \
    fields, \
    marshal_with
from sqlalchemy.exc import IntegrityError

from app import app
from app import db
from utils import valid_email, \
    get_object_or_abort, \
    get_unique_regex_from_error, get_paginated_list
from .models import User

api = Api(app, prefix='/api/users')


def email(email_str):
    """Return email_str if valid, raise an exception in other case."""
    if valid_email(email_str):
        return email_str
    else:
        raise ValueError('{} is not a valid email'.format(email_str))


post_parser = reqparse.RequestParser()
post_parser.add_argument(
    'email',
    dest='email',
    type=email,
    required=True,
    help='Email is not valid',
)
post_parser.add_argument(
    'first_name',
    dest='first_name',
    required=True,
    type=str,
    help='The user\'s first_name',
)
post_parser.add_argument(
    'last_name',
    dest='last_name',
    required=True,
    type=str,
    help='The user\'s last_name',
)
post_parser.add_argument(
    'fleet_id',
    dest='fleet_id',
    required=True,
    type=int,
    help='The fleet\'s id',
)


user_fields = {
    'id': fields.Integer,
    'email': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'fleet_id': fields.Integer
}

users_fields = {
    'count': fields.Integer,
    'previous': fields.String,
    'next': fields.String,
    'results': fields.Nested({
        **user_fields
    })
}


class UsersResource(Resource):

    @marshal_with(users_fields)
    def get(self):
        fleet_id = request.args.get('fleet_id')
        if fleet_id and fleet_id.isdigit():
            users = User.query.filter(User.fleet_id == fleet_id)
        else:
            users = User.query
        return get_paginated_list(request, users, per_page=5)

    @marshal_with(user_fields)
    def post(self):
        args = post_parser.parse_args()

        try:
            user = User(**args)
            db.session.add(user)
            db.session.commit()
        except IntegrityError as e:
            unique_regex = get_unique_regex_from_error(str(e.orig))
            if unique_regex:
                abort(400, message={"email": "Object with this email already exist"})
            else:
                app.logger.info(str(e))
                raise
        else:
            return user, 201


api.add_resource(UsersResource, '/')


class UserResource(Resource):

    @marshal_with(user_fields)
    def get(self, user_id):
        user = get_object_or_abort(User, user_id)
        return user, 200

    @marshal_with(user_fields)
    def put(self, user_id):
        user = get_object_or_abort(User, user_id)

        args = post_parser.parse_args()

        try:
            for field, val in args.items():
                setattr(user, field, val)

            db.session.add(user)
            db.session.commit()
        except IntegrityError as e:
            unique_regex = get_unique_regex_from_error(str(e.orig))
            if unique_regex:
                abort(400, message={"email": "Object with this email already exist"})
            else:
                raise
        else:
            return user, 200

    def delete(self, user_id):
        user = get_object_or_abort(User, user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204


api.add_resource(UserResource, '/<int:user_id>/')
