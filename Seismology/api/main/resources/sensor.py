from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import SensorModel
from main.auth.decorators import admin_required


class Sensor(Resource):

    @admin_required
    def get(self, id):
        sensor = db.session.query(SensorModel).get_or_404(id)
        return sensor.to_json()

    @admin_required
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

    @admin_required
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

    @admin_required
    def get(self):
        page = 1
        per_page = 50
        sensors = db.session.query(SensorModel)
        filters = request.get_json().items()
        for key, value in filters:
            if key == "active":
                sensors = sensors.filter(SensorModel.active == value)
            if key == "status":
                sensors = sensors.filter(SensorModel.status == value)
            if key == "user":
                if value:
                    sensors = sensors.filter(SensorModel.userId != None)
                else:
                    sensors = sensors.filter(SensorModel.userId == None)
            if key == "userId":
                sensors = sensors.filter(SensorModel.userId == value)
            if key =="sort_by":
                if value == "name":
                    sensors = sensors.order_by(SensorModel.name)
                if value == "name.desc":
                    sensors = sensors.order_by(SensorModel.name.desc())
                if value == "status":
                    sensors = sensors.order_by(SensorModel.status)
                if value == "status.desc":
                    sensors = sensors.order_by(SensorModel.status.desc())
                if value == "active":
                    sensors = sensors.order_by(SensorModel.active)
                if value == "active.desc":
                    sensors = sensors.order_by(SensorModel.active.desc())
            if key == "page":
                page = value
            if key == "per_page":
                per_page = value
        sensors = sensors.paginate(page, per_page, True, 100)
        return jsonify({ 'sensors': [sensor.to_json() for sensor in sensors.items] })

    @admin_required
    def post(self):
        sensor = SensorModel.from_json(request.get_json())
        try:
            db.session.add(sensor)
            db.session.commit()
            return  sensor.to_json(), 201
        except Exception as error:
            return str(error), 400
