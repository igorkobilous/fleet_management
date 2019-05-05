from app import db
from fleet.models import Fleet
from test import BaseTestCase, generate_test_data
from user.models import User
from vehicle.models import Vehicle


class FleetModelTestCase(BaseTestCase):

    def setUp(self):
        super(FleetModelTestCase, self).setUp()

        generate_test_data()

    def test_base_model_operation(self):

        fleets_count = len(Fleet.query.all())
        fleet = Fleet(name="Valid fleet")
        db.session.add(fleet)
        db.session.commit()

        self.assertEqual(fleets_count + 1, len(Fleet.query.all()))
        self.assertIsNotNone(fleet.id)
        self.assertEqual(fleet.name, "Valid fleet")

        fleet.name = "New valid fleet"

        db.session.add(fleet)
        db.session.commit()

        fleet = Fleet.query.filter(Fleet.name == "New valid fleet").first()
        self.assertEqual(fleet.name, "New valid fleet")


        db.session.delete(fleet)
        db.session.commit()
        self.assertEqual(fleets_count, len(Fleet.query.all()))


class UserModelTestCase(BaseTestCase):

    def setUp(self):
        super(UserModelTestCase, self).setUp()

        generate_test_data()

    def test_base_model_operation(self):
        fleet = Fleet.query.first()

        users_count = len(User.query.all())
        user = User(email="test_user@test.com",
                     first_name="Test",
                     last_name="Test",
                     fleet_id=fleet.id)
        db.session.add(user)
        db.session.commit()

        self.assertEqual(users_count + 1, len(User.query.all()))
        self.assertIsNotNone(user.id)
        self.assertEqual(user.email, "test_user@test.com")
        self.assertIn(user, fleet.users)

        user.first_name = "New Test"

        db.session.add(user)
        db.session.commit()

        user = User.query.filter(User.email == "test_user@test.com").first()
        self.assertEqual(user.first_name, "New Test")


        db.session.delete(user)
        db.session.commit()
        self.assertEqual(users_count, len(Fleet.query.all()))


class VehicleModelTestCase(BaseTestCase):

    def setUp(self):
        super(VehicleModelTestCase, self).setUp()

        generate_test_data()

    def test_base_model_operation(self):
        fleet = Fleet.query.first()
        user = User.query.filter(User.fleet_id == fleet.id).first()

        vehicles_count = len(Vehicle.query.all())
        vehicle = Vehicle(name="Lexus IS250",
                          user_id=user.id,
                          fleet_id=fleet.id)
        db.session.add(vehicle)
        db.session.commit()

        self.assertEqual(vehicles_count + 1, len(Vehicle.query.all()))
        self.assertIsNotNone(vehicle.id)
        self.assertEqual(vehicle.name, "Lexus IS250")
        self.assertIn(vehicle, fleet.vehicles)
        self.assertIn(vehicle, user.vehicles)

        vehicle.name = "Ford Focus"

        db.session.add(vehicle)
        db.session.commit()

        vehicle = Vehicle.query.filter(Vehicle.id == vehicle.id).first()
        self.assertEqual(vehicle.name, "Ford Focus")


        db.session.delete(vehicle)
        db.session.commit()
        self.assertEqual(vehicles_count, len(Vehicle.query.all()))
