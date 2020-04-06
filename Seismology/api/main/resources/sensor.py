from flask_restful import Resource
from flask import request


SENSORS = {
    1: {'id': '1', 'name': 'Mendoza, Argentina', 'status':'enabled'},
    2: {'id': '2', 'name': 'Santiago, Chile', 'status':'disabled'},
}


class Sensor(Resource):

    def get(self, id):
        if int(id) in SENSORS:
            return SENSORS[int(id)]
        return 'Sensor not found', 404

    def put(self, id):
        if int(id) in SENSORS:
            sensor = SENSORS[int(id)]
            data = request.get_json()
            sensor.update(data)
            return sensor, 201
        return 'Sensor not found', 404

    def delete(self, id):
        if int(id) in SENSORS:
            del SENSORS[int(id)]
            return 'Sensor succesfully deleted', 204
        return 'Sensor not found', 404

class Sensors(Resource):

    def get(self):
        return SENSORS

    def post(self):
        sensor = request.get_json()
        id = int(max(SENSORS.keys())) + 1
        SENSORS[id] = sensor
        return SENSORS[id], 201
