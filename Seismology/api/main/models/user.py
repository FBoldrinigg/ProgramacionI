from .. import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), unique = True, nullable = False)
    password = db.Column(db.String(100), nullable = False)
    admin = db.Column(db.Boolean, nullable = False)
    sensors = db.relationship('Sensor', back_populates = "user")

    @property
    def plain_password(self):
        raise AtributeError("Can't read password")

    @plain_password.setter
    def plain_password(self, password):
        self.password = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return "<User: %r >" % (self.email)

    def to_json(self):
        user_json = {
            'id':self.id,
            'email': str(self.email)
        }
        return user_json

    @staticmethod
    def from_json(user_json):
        id = user_json.get('id')
        email = user_json.get('email')
        password = user_json.get('password')
        admin = user_json.get('admin')
        return User(id = id, email = email, plain_password = password, admin = admin)
