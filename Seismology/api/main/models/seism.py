from .. import db


class Seism(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    datetime = db.Column(db.DateTime, nullable = False)
    depth = db.Column(db.Integer, nullable = False)
    magnitude = db.Column(db.DECIMAL(4, 3), nullable = False)
    latitude = db.Column(db.String(100), nullable = False)
    longitude = db.Column(db.String(100), nullable = False)
    verified = db.Column(db.Boolean, nullable = False)

    def __repr__(self):
        return "<Seism: %r %r %r %r >" % (self.depth, self.magnitude, self.latitude, self.longitude)

        def to_json(self):
            seism_json = {
                'id':self.id,
                'datetime': self.datetime.strftime("%Y-%m-%d, %H:%M:%S"),
                'depth': self.depth,
                'magnitude': self.magnitude,
                'latitude': str(self.latitude),
                'longitude': str(self.longitude),
                'verified': self.verified
            }
            return seism_json

        def from_json(seism_json):
            id = seism_json.get('id')
            datetime = seism_json.get('datetime')
            depth = seism_json.get('depth')
            magnitude = seism_json.get('magnitude')
            latitude = seism_json.get('latitude')
            longitude = seism_json.get('longitude')
            verified = seism_json.get('verified')
            return Seism(id = id, datetime = datetime, depth = depth, magnitude = magnitude, latitude =  latitude, longitude = longitude, verified = verified)
