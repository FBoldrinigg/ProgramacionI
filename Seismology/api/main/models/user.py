from .. import db


class User(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), nullable = False)
    password = db.Column(db.String(100), nullable = False)
    admin = db.Column(db.Boolean, nullable = False)
    # sensors = db.relationship('Sensor', back_populates = "user", passive_deletes="all")

    def __repr__(self):
        return "<User: %r >" % (self.email)

    def to_json(self):
        user_json = {
            'id':self.id,
            'email': str(self.email),
            'password': str(self.password),
            'admin': self.admin
        }
        return user_json

    def from_json(user_json):
        id = user_json.get('id')
        email = user_json.get('email')
        password = user_json.get('password')
        admin = user_json.get('admin')
        return User(id = id, email = email, password = password, admin = admin)
