from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import SeismModel, SensorModel
import time
from random import uniform, random, randint, uniform


class VerifiedSeism(Resource):

    def get(self, id):
        seism = db.session.query(SeismModel).get_or_404(id)
        if seism.verified:
            return seism.to_json()
        else:
            return 'Forbidden access', 403

class VerifiedSeisms(Resource):

    def get(self):
        seisms = db.session.query(SeismModel).filter(SeismModel.verified == True)
        filters = request.get_json().items()
        for key, value in filters:
            if key == "datetime":
                seisms = seisms.filter(SeismModel._dt == value)
            if key == "sensorId":
                seisms = seisms.filter(SeismModel.sensorId == value)
            if key == "latitude":
                seisms = seisms.filter(SeismModel.latitude == value)
            if key == "longitude":
                seisms = seisms.filter(SeismModel.longitude == value)
            if key == "depth":
                seisms = seisms.filter(SeismModel.depth == value)
            if key == "magnitude":
                seisms = seisms.filter(SeismModel.magnitude == value)
        seisms.all()
        return jsonify({'Verified-Seisms': [seism.to_json() for seism in seisms]})

    def post(self):
        sensors = db.session.query(SensorModel).all()
        sensorsId = []
        for sensor in sensors:
            sensorsId.append(sensor.id)
        if sensorsId:
            value_sensor = {
            'datetime': time.strftime(r"%Y-%m-%d %H:%M:%S", time.localtime()),
            'depth': randint(5,250) ,
            'magnitude': round(uniform(2.0,5.5), 1),
            'latitude': uniform(-180,180),
            'longitude': uniform(-90, 90),
            'verified': True,
            'sensorId': sensorsId[randint(0, len(sensorsId) - 1)]
            }
            seism = SeismModel.from_json(value_sensor)
            db.session.add(seism)
            db.session.commit()
            return seism.to_json(), 201
        else:
            return "No sensors found, can't create seism", 400


class UnverifiedSeism(Resource):

    def get(self, id):
        seism = db.session.query(SeismModel).get_or_404(id)
        if not seism.verified:
            return seism.to_json()
        else:
            return 'Forbidden access', 403

    def delete(self, id):
        seism = db.session.query(SeismModel).get_or_404(id)
        if not seism.verified:
            db.session.delete(seism)
            db.session.commit()
            return "Unverified seism deleted succesfully", 204
        else:
            return 'Forbidden access', 403

    def put(self, id):
        seism = db.session.query(SeismModel).get_or_404(id)
        if not seism.verified:
            for key, value in request.get_json().items():
                setattr(seism, key, value)
            db.session.add(seism)
            try:
                db.session.commit()
                return seism.to_json(), 201
            except Exception as error:
                return str(error), 400
        else:
            return 'Forbidden access', 403


class UnverifiedSeisms(Resource):

    def get(self):
        seisms = db.session.query(SeismModel).filter(SeismModel.verified == False)
        filters = request.get_json().items()
        for key, value in filters:
            if key == "datetime":
                seisms = seisms.filter(SeismModel._dt == value)
            if key == "sensorId":
                seisms = seisms.filter(SeismModel.sensorId == value)
            if key == "latitude":
                seisms = seisms.filter(SeismModel.latitude == value)
            if key == "longitude":
                seisms = seisms.filter(SeismModel.longitude == value)
            if key == "depth":
                seisms = seisms.filter(SeismModel.depth == value)
            if key == "magnitude":
                seisms = seisms.filter(SeismModel.magnitude == value)
        seisms.all()
        return jsonify({'Unverified-Seisms': [seism.to_json() for seism in seisms]})

    def post(self):
        sensors = db.session.query(SensorModel).all()
        sensorsId = []
        for sensor in sensors:
            sensorsId.append(sensor.id)
        if sensorsId:
            value_sensor = {
            'datetime': time.strftime(r"%Y-%m-%d %H:%M:%S", time.localtime()),
            'depth': randint(5,250) ,
            'magnitude': round(uniform(2.0,5.5), 1),
            'latitude': uniform(-180,180),
            'longitude': uniform(-90, 90),
            'verified': False,
            'sensorId': sensorsId[randint(0, len(sensorsId) - 1)]
            }
            seism = SeismModel.from_json(value_sensor)
            db.session.add(seism)
            db.session.commit()
            return seism.to_json(), 201
        else:
            return "No sensors found, can't create seism", 400
