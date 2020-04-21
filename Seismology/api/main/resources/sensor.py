from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import SensorModel


class Sensor(Resource):

    def get(self, id):
        sensor = db.session.query(SensorModel).get_or_404(id)
        return sensor.to_json()

    def put(self, id):
        sensor = db.session.query(SensorModel).get_or_404(id)
        for key, value in request.get_json().items():
            setattr(sensor, key, value)
        db.session.add(sensor)
        try:
            db.session.commit()
            return sensor.to_json(), 201
        except Exception as error:
            return str(error), 400

    def delete(self, id):
        sensor = db.session.query(SensorModel).get_or_404(id)
        db.session.delete(sensor)
        try:
            db.session.commit()
            return "Sensor deleted succesfully", 204
        except Exception as error:
            db.session.rollback()
            return str(error), 409


class Sensors(Resource):

    def get(self):
        sensors = db.session.query(SensorModel)
        filters = request.get_json().items()
        for key, value in filters:
            if key == "ip":
                sensors = sensors.filter(SensorModel.ip == value)
            if key == "port":
                sensors = sensors.filter(SensorModel.port == value)
            if key == "active":
                sensors = sensors.filter(SensorModel.active == value)
            if key == "status":
                sensors = sensors.filter(SensorModel.status == value)
            if key == "userId":
                sensors = sensors.filter(SensorModel.userId == value)
        sensors.all()
        return jsonify({ 'sensors': [sensor.to_json() for sensor in sensors] })

    def post(self):
        sensor = SensorModel.from_json(request.get_json())
        try:
            db.session.add(sensor)
            db.session.commit()
            return  sensor.to_json(), 201
        except Exception as error:
            return str(error), 400
