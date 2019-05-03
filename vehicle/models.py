import random
import string

from app import db


def serial_number_generator(size=16, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class Vehicle(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    serial_number = db.Column(db.String(16))
    name = db.Column(db.String(255))

    fleet_id = db.Column(db.Integer, db.ForeignKey('fleet.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, *args, **kwargs):
        super(Vehicle, self).__init__(*args, **kwargs)
        if not self.serial_number:
            self.serial_number = serial_number_generator()

    def __repr__(self):
        return '<Vehicle id: {}, serial_number: {}>'.format(self.id, self.serial_number)
