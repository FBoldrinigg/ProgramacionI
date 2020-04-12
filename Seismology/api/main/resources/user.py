from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UserModel


class User(Resource):

    def get(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        return user.to_json()

    def put(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        for key, value in request.get_json().items():
            setattr(user, key, value)
        db.session.add(user)
        db.session.commit()
        return user.to_json(), 201

    def delete(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return "User deleted succesfully", 204

class Users(Resource):

    def get(self):
        users = db.session.query(UserModel).all()
        return jsonify({'Users': [user.to_json() for user in users]})

    def post(self):
        user = UserModel.from_json(request.get_json())
        db.session.add(user)
        db.session.commit()
        return user.to_json(), 201
