import json

from app import db
from fleet.models import Fleet
from test import BaseTestCase, generate_test_data
from user.models import User
from vehicle.models import Vehicle


class FleetFunctionsTestCase(BaseTestCase):

    def setUp(self):
        super(FleetFunctionsTestCase, self).setUp()

        generate_test_data()

    def test_fleet_list(self):
        response = self.client.get('/api/fleets/', content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('next', response.json.keys())
        self.assertIn('previous', response.json.keys())
        self.assertIn('count', response.json.keys())
        self.assertIn('results', response.json.keys())
        self.assertEqual(response.json['count'], len(Fleet.query.all()))
        self.assertEqual(response.json['count'], 3)

    def test_create_fleet(self):
        data = dict(name='New valid test name')

        response = self.client.post('/api/fleets/',
                                    data=json.dumps(data),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(type(response.json), dict)
        self.assertIn('id', response.json.keys())
        self.assertEqual(response.json['name'], data['name'])

        fleets_count = len(Fleet.query.all())
        fleet = Fleet.query.get(response.json['id'])
        db.session.delete(fleet)
        db.session.commit()
        self.assertEqual(fleets_count - 1, len(Fleet.query.all()))

    def test_create_fleet_with_occupied_name(self):
        data = dict(name='First fleet')

        response = self.client.post('/api/fleets/',
                                    data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message']['name'], 'Object with this name already exist')

    def test_get_detail_fleet(self):
        fleet = Fleet.query.filter(Fleet.name == 'First fleet').first()

        response = self.client.get('/api/fleets/{}/'.format(fleet.id),
                                   content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.json), dict)
        self.assertIn('id', response.json.keys())
        self.assertEqual(response.json['name'], fleet.name)
        self.assertEqual(response.json['id'], fleet.id)

    def test_update_fleet(self):
        fleet = Fleet.query.filter(Fleet.name == 'First fleet').first()
        fleet_name = fleet.name
        data = dict(name="Fleet first")

        response = self.client.put('/api/fleets/{}/'.format(fleet.id),
                                   data=json.dumps(data),
                                   content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.json), dict)
        self.assertIn('id', response.json.keys())
        self.assertNotEqual(response.json['name'], fleet_name)
        self.assertEqual("Fleet first",response.json['name'] )

    def test_update_fleet_with_occupied_name(self):
        fleet = Fleet.query.filter(Fleet.name == 'Third fleet').first()
        response = self.client.put('/api/fleets/{}/'.format(fleet.id),
                                   data=json.dumps(dict(name='Second fleet')),
                                   content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message']['name'], 'Object with this name already exist')

    def test_delete_fleet(self):
        data = dict(name='New valid test second name')
        response = self.client.post('/api/fleets/',
                                    data=json.dumps(data),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 201)
        fleet_id = response.json['id']

        fleets_count = len(Fleet.query.all())

        response = self.client.delete('/api/fleets/{}/'.format(fleet_id),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(fleets_count - 1, len(Fleet.query.all()))



class UserFunctionsTestCase(BaseTestCase):

    def setUp(self):
        super(UserFunctionsTestCase, self).setUp()

        generate_test_data()

    def test_users_list(self):
        response = self.client.get('/api/users/', content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('next', response.json.keys())
        self.assertIn('previous', response.json.keys())
        self.assertIn('count', response.json.keys())
        self.assertIn('results', response.json.keys())
        self.assertEqual(response.json['count'], len(User.query.all()))
        self.assertEqual(response.json['count'], 3)

    def test_filtered_users_list(self):
        fleet = Fleet.query.filter(Fleet.name == 'First fleet').first()

        response = self.client.get('/api/users/?fleet_id={}'.format(fleet.id),
                                   content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('next', response.json.keys())
        self.assertIn('previous', response.json.keys())
        self.assertIn('count', response.json.keys())
        self.assertIn('results', response.json.keys())
        self.assertEqual(response.json['count'], len(User.query.filter(User.fleet_id == fleet.id).all()))
        self.assertEqual(response.json['count'], 2)

    def test_create_user(self):

        fleet = Fleet.query.first()
        data = dict(email='new_f_first@test.com',
                    first_name='First',
                    last_name='First',
                    fleet_id=fleet.id)

        response = self.client.post('/api/users/',
                                    data=json.dumps(data),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(type(response.json), dict)
        self.assertIn('id', response.json.keys())
        self.assertEqual(response.json['email'], data['email'])
        self.assertEqual(response.json['fleet_id'], data['fleet_id'])

        users_count = len(User.query.all())
        user = User.query.get(response.json['id'])
        db.session.delete(user)
        db.session.commit()
        self.assertEqual(users_count - 1, len(User.query.all()))

    def test_create_user_with_occupied_name(self):

        fleet = Fleet.query.first()
        data = dict(email='f_first_user@test.com',
                    first_name='First',
                    last_name='First',
                    fleet_id=fleet.id)

        response = self.client.post('/api/users/',
                                    data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message']['email'], 'Object with this email already exist')

    def test_get_user_detail(self):
        user = User.query.filter(User.email == 'f_first_user@test.com').first()

        response = self.client.get('/api/users/{}/'.format(user.id),
                                   content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.json), dict)
        self.assertIn('id', response.json.keys())
        self.assertEqual(response.json['email'], user.email)
        self.assertEqual(response.json['id'], user.id)

    def test_update_user(self):
        user = User.query.filter(User.email == 'f_first_user@test.com').first()
        user_email = user.email
        data = dict(email="fu_first_user@test.com",
                    first_name=user.first_name,
                    last_name=user.last_name,
                    fleet_id=user.fleet_id
                    )

        response = self.client.put('/api/users/{}/'.format(user.id),
                                   data=json.dumps(data),
                                   content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.json), dict)
        self.assertIn('id', response.json.keys())
        self.assertNotEqual(response.json['email'], user_email)
        self.assertEqual("fu_first_user@test.com", response.json['email'])

    def test_update_user_with_occupied_name(self):
        user = User.query.filter(User.email == 's_first_user@test.com').first()
        data = dict(email="f_second_user@test.com",
                    first_name=user.first_name,
                    last_name=user.last_name,
                    fleet_id=user.fleet_id
                    )
        response = self.client.put('/api/users/{}/'.format(user.id),
                                   data=json.dumps(data),
                                   content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message']['email'], 'Object with this email already exist')

    def test_delete_user(self):
        fleet = Fleet.query.first()
        data = dict(email='new_f_first@test.com',
                    first_name='First',
                    last_name='First',
                    fleet_id=fleet.id)
        response = self.client.post('/api/users/',
                                    data=json.dumps(data),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 201)
        user_id = response.json['id']

        users_count = len(User.query.all())

        response = self.client.delete('/api/users/{}/'.format(user_id),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(users_count - 1, len(User.query.all()))


class VehicleFunctionsTestCase(BaseTestCase):
    def setUp(self):
        super(VehicleFunctionsTestCase, self).setUp()

        generate_test_data()

    def test_vehicles_list(self):
        response = self.client.get('/api/vehicles/', content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('next', response.json.keys())
        self.assertIn('previous', response.json.keys())
        self.assertIn('count', response.json.keys())
        self.assertIn('results', response.json.keys())
        self.assertEqual(response.json['count'], len(Vehicle.query.all()))
        self.assertEqual(response.json['count'], 2)

    def test_filtered_vehicles_list(self):
        fleet = Fleet.query.filter(Fleet.name == 'First fleet').first()

        response = self.client.get('/api/vehicles/?fleet_id={}'.format(fleet.id),
                                   content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('next', response.json.keys())
        self.assertIn('previous', response.json.keys())
        self.assertIn('count', response.json.keys())
        self.assertIn('results', response.json.keys())
        self.assertEqual(response.json['count'], len(Vehicle.query.filter(Vehicle.fleet_id == fleet.id).all()))
        self.assertEqual(response.json['count'], 1)

    #=======================================================================================

    def test_create_vehicle(self):

        fleet = Fleet.query.first()
        user = User.query.filter(User.fleet_id == fleet.id).first()
        data = dict(name="Toyota camry",
                    user_id=user.id,
                    fleet_id=fleet.id)

        response = self.client.post('/api/vehicles/',
                                    data=json.dumps(data),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(type(response.json), dict)
        self.assertIn('id', response.json.keys())
        self.assertIn('serial_number', response.json.keys())
        self.assertEqual(response.json['name'], data['name'])
        self.assertEqual(response.json['user_id'], data['user_id'])
        self.assertEqual(response.json['fleet_id'], data['fleet_id'])

        vehicles_count = len(Vehicle.query.all())
        vehicle = Vehicle.query.get(response.json['id'])
        db.session.delete(vehicle)
        db.session.commit()
        self.assertEqual(vehicles_count- 1, len(Vehicle.query.all()))


    def test_get_vehicle_detail(self):
        vehicle = Vehicle.query.first()

        response = self.client.get('/api/vehicles/{}/'.format(vehicle.id),
                                   content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.json), dict)
        self.assertIn('id', response.json.keys())
        self.assertEqual(response.json['id'], vehicle.id)
        self.assertEqual(response.json['name'], vehicle.name)
        self.assertEqual(response.json['user_id'], vehicle.user_id)
        self.assertEqual(response.json['fleet_id'], vehicle.fleet_id)
        self.assertEqual(response.json['serial_number'], vehicle.serial_number)

    def test_update_vehicle(self):
        vehicle = Vehicle.query.first()
        vehicle_name = vehicle.name
        data = dict(name="VW Passat b7",
                    fleet_id=vehicle.fleet_id,
                    user_id=vehicle.user_id
                    )

        response = self.client.put('/api/vehicles/{}/'.format(vehicle.id),
                                   data=json.dumps(data),
                                   content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.json), dict)
        self.assertIn('id', response.json.keys())
        self.assertNotEqual(response.json['name'], vehicle_name)
        self.assertEqual("VW Passat b7", response.json['name'])

    def test_delete_vehicle(self):
        fleet = Fleet.query.first()
        user = User.query.filter(User.fleet_id == fleet.id).first()

        data = dict(name="Honda accord",
                    user_id=user.id,
                    fleet_id=fleet.id)
        response = self.client.post('/api/vehicles/',
                                    data=json.dumps(data),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 201)
        vehicle_id = response.json['id']

        vehicles_count = len(Vehicle.query.all())

        response = self.client.delete('/api/vehicles/{}/'.format(vehicle_id),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(vehicles_count - 1, len(Vehicle.query.all()))
