from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import SeismModel


class VerifiedSeism(Resource):

    def get(self, id):
        seism = db.session.query(SeismModel).get_or_404(id)
        return seism.to_json()


class VerifiedSeisms(Resource):

    def get(self):
        seisms = db.session.query(SeismModel).filter(SeismModel.verified == True).all()
        return jsonify({'Verified-Seisms': [seism.to_json() for seism in seisms]})


class UnverifiedSeism(Resource):

    def get(self, id):
        seism = db.session.query(SeismModel).get_or_404(id)
        return seism.to_json()

    def delete(self, id):
        seism = db.session.query(SeismModel).get_or_404(id)
        db.session.delete(seism)
        db.session.commit()
        return "Unverified seism deleted succesfully", 204

    def put(self, id):
        seism = db.session.query(SeismModel).get_or_404(id)
        for key, value in request.get_json().items():
            setattr(seism, key, value)
        db.session.add(seism)
        db.session.commit()
        return seism.to_json(), 201


class UnverifiedSeisms(Resource):

    def get(self):
        seisms = db.session.query(SeismModel).filter(SeismModel.verified == False).all()
        return jsonify({'Unverified-Seisms': [seism.to_json for seism in seisms]})
