from app import db


class Fleet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), unique=True)

    users = db.relationship("User")
    vehicles = db.relationship("Vehicle")

    def __repr__(self):
        return '<Fleet id: {}, name: {}>'.format(self.id, self.name)
