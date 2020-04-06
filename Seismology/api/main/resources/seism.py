from flask_restful import Resource
from flask import request


VERIFIED_SEISMS = {
    1: {'id': '1', 'datetime': '03/01/2020', 'magnitude':'5.6'},
    2: {'id': '2', 'datetime': '06/02/2020', 'magnitude':'8.3'},
}

UNVERIFIED_SEISMS = {
    1: {'id': '1', 'datetime': '08/01/2020', 'magnitude':'2.4'},
    2: {'id': '2', 'datetime': '07/02/2020', 'magnitude':'3.3'},
    3: {'id': '3', 'datetime': '07/03/2020', 'magnitude':'1.8'}
}


class VerifiedSeism(Resource):

    def get(self, id):
        if int(id) in VERIFIED_SEISMS:
            return VERIFIED_SEISMS[int(id)]
        return 'Verified seism not found', 404


class VerifiedSeisms(Resource):

    def get(self):
        return VERIFIED_SEISMS


class UnverifiedSeism(Resource):

    def get(self, id):
        if int(id) in UNVERIFIED_SEISMS:
            return UNVERIFIED_SEISMS[int(id)]
        return 'Unverified seism not found', 404

    def delete(self, id):
        if int(id) in UNVERIFIED_SEISMS:
            del UNVERIFIED_SEISMS[int(id)]
            return 'Unverified seism succesfully deleted', 204
        return 'Unverified seism not found', 404

    def put(self, id):
        if int(id) in UNVERIFIED_SEISMS:
            unvSeism = UNVERIFIED_SEISMS[int(id)]
            data = request.get_json()
            unvSeism.update(data)
            return unvSeism, 201
        return 'Unverified seism not found', 404


class UnverifiedSeisms(Resource):

    def get(self):
        return UNVERIFIED_SEISMS
