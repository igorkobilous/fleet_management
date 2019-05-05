from flask_testing import TestCase

from app import app
from app import db
from fleet.models import Fleet
from user.models import User
from vehicle.models import Vehicle
from fleet.resourses import api as fleet_api
from user.resourses import api as user_api
from vehicle.resourses import api as vehicle_api


class BaseTestCase(TestCase):
    """A base test case"""

    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


def generate_test_data():
    fleet_first = Fleet(name='First fleet')
    fleet_second = Fleet(name='Second fleet')
    fleet_third = Fleet(name='Third fleet')
    db.session.add_all([
        fleet_first,
        fleet_second,
        fleet_third
    ])
    db.session.commit()

    user_first = User(email='f_first_user@test.com',
                      first_name='First',
                      last_name='First',
                      fleet_id=fleet_first.id)
    user_second = User(email='f_second_user@test.com',
                       first_name='Second',
                       last_name='Second',
                       fleet_id=fleet_first.id)
    user_third = User(email='s_first_user@test.com',
                      first_name='First',
                      last_name='First',
                      fleet_id=fleet_second.id)
    db.session.add_all([
        user_first,
        user_second,
        user_third
    ])
    db.session.commit()

    vehicle_first = Vehicle(name='Audi Q5',
                            fleet_id=fleet_first.id,
                            user_id=user_first.id)
    vehicle_second = Vehicle(name='BMW X5',
                             fleet_id=fleet_second.id,
                             user_id=user_third.id)
    db.session.add_all([
        vehicle_first,
        vehicle_second
    ])
    db.session.commit()
