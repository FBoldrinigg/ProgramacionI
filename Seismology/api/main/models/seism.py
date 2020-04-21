from .. import db
from datetime import datetime as dtm
from .sensor import Sensor as SensorModel


class Seism(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    _dt = db.Column("datetime", db.DateTime, nullable = False)
    depth = db.Column(db.Integer, nullable = False)
    magnitude = db.Column(db.Float, nullable = False)
    latitude = db.Column(db.String(100), nullable = False)
    longitude = db.Column(db.String(100), nullable = False)
    verified = db.Column(db.Boolean, nullable = False)
    sensorId = db.Column(db.Integer, db.ForeignKey('sensor.id', ondelete = 'RESTRICT'), nullable = False)
    sensor = db.relationship('Sensor', back_populates = "seisms", uselist = False, single_parent = True)

    @property
    def dt(self):
        return self._dt

    @dt.setter
    def setDt(self, value):
        newValue = dtm.strptime(value, "%Y-%m-%d %H:%M:%S")
        self._dt = newValue

    def __repr__(self):
        return "<Seism: %r %r %r %r >" % (self.depth, self.magnitude, self.latitude, self.longitude)

    def to_json(self):
        sensor = db.session.query(SensorModel).get_or_404(self.sensorId)
        seism_json = {
            'id':self.id,
            'datetime': self._dt.strftime("%Y-%m-%d %H:%M:%S"),
            'depth': self.depth,
            'magnitude': self.magnitude,
            'latitude': str(self.latitude),
            'longitude': str(self.longitude),
            'verified': self.verified,
            'sensor': sensor.to_json()
        }
        return seism_json

    @staticmethod
    def from_json(seism_json):
        id = seism_json.get('id')
        dt = dtm.strptime(seism_json.get('datetime'), "%Y-%m-%d %H:%M:%S")
        depth = seism_json.get('depth')
        magnitude = seism_json.get('magnitude')
        latitude = seism_json.get('latitude')
        longitude = seism_json.get('longitude')
        verified = seism_json.get('verified')
        sensorId = seism_json.get('sensorId')
        return Seism(id = id, _dt = dt, depth = depth, magnitude = magnitude, latitude =  latitude, longitude = longitude, verified = verified, sensorId = sensorId)
