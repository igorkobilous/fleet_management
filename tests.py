import unittest
import os
from app import app, db


basedir = os.path.abspath(os.path.dirname(__file__))


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_one(self):
        response = self.app.get('/api/users/')
        print(response.status)
        assert response.status == '200 OK'


if __name__ == '__main__':
    unittest.main()
