from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import SeismModel, SensorModel
import time
from random import uniform, random, randint, uniform
from main.auth.decorators import admin_required
from flask_jwt_extended import jwt_required, get_jwt_claims, get_jwt_identity


class VerifiedSeism(Resource):

    def get(self, id):
        seism = db.session.query(SeismModel).get_or_404(id)
        if seism.verified:
            return seism.to_json()
        else:
            return 'Forbidden access', 403

class VerifiedSeisms(Resource):

    def get(self):
        page = 1
        per_page = 1000
        seisms = db.session.query(SeismModel).filter(SeismModel.verified == True)
        filters = request.get_json().items()
        for key, value in filters:
            if key == "datetime":
                seisms = seisms.filter(SeismModel._dt.like('%' + value + '%'))
            if key == "sensorId":
                seisms = seisms.filter(SeismModel.sensorId == value)
            if key == "sensor.name":
                seisms = seisms.join(SeismModel.sensor).filter(SensorModel.name.like('%' + value + '%'))
            if key == "magnitude":
                seisms = seisms.filter(SeismModel.magnitude == value)
            if key == "sort_by":
                    if value == "datetime":
                        seisms = seisms.order_by(SeismModel._dt)
                    if value == "datetime.desc":
                        seisms = seisms.order_by(SeismModel._dt.desc())
                    if value == "sensor.name":
                        seisms = seisms.join(SeismModel.sensor).order_by(SensorModel.name)
                    if value == "sensor.name.desc":
                        seisms = seisms.join(SeismModel.sensor).order_by(SensorModel.name.desc())
            if key == "page":
                page = value
            if key == "per_page":
                per_page = value
        seisms = seisms.paginate(page, per_page, True, 10000)
        return jsonify({'Verified-Seisms': [seism.to_json() for seism in seisms.items]})

    """
    # Descomentarla para añadir sismos verificados a la db para testear #
    @jwt_required
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
    """

class UnverifiedSeism(Resource):

    @jwt_required
    def get(self, id):
        seism = db.session.query(SeismModel).get_or_404(id)
        if not seism.verified:
            return seism.to_json()
        else:
            return 'Forbidden access', 403

    @jwt_required
    def delete(self, id):
        seism = db.session.query(SeismModel).get_or_404(id)
        if not seism.verified:
            db.session.delete(seism)
            db.session.commit()
            return "Unverified seism deleted succesfully", 204
        else:
            return 'Forbidden access', 403

    @jwt_required
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

    @jwt_required
    def get(self):
        page =  1
        per_page = 50
        seisms = db.session.query(SeismModel).filter(SeismModel.verified == False)
        filters = request.get_json().items()
        current_user_id = get_jwt_identity()
        seisms = seisms.join(SeismModel.sensor).filter(SensorModel.userId == current_user_id)
        for key, value in filters:
            if key == "sensorId":
                seisms = seisms.filter(SeismModel.sensorId == value)
            if key == "sort_by":
                    if value == "datetime":
                        seisms = seisms.order_by(SeismModel._dt)
                    if value == "datetime.desc":
                        seisms = seisms.order_by(SeismModel._dt.desc())
            if key == "page":
                page = value
            if key == "per_page":
                per_page = value
        seisms = seisms.paginate(page, per_page, True, 50)
        return jsonify({'Unverified-Seisms': [seism.to_json() for seism in seisms.items]})

    @jwt_required
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
