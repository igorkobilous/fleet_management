from app import db


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(100), unique=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))

    fleet_id = db.Column(db.Integer, db.ForeignKey('fleet.id'), nullable=False)

    vehicles = db.relationship("Vehicle")

    def __repr__(self):
        return '<User id: {}, email: {}>'.format(self.id, self.email)
