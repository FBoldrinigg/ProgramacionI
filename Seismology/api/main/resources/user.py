from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UserModel
from main.auth.decorators import admin_required
from flask_jwt_extended import jwt_required


class User(Resource):

    @admin_required
    def get(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        return user.to_json()

    @admin_required
    def put(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        for key, value in request.get_json().items():
            setattr(user, key, value)
        db.session.add(user)
        db.session.commit()
        return user.to_json(), 201

    @admin_required
    def delete(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return "User deleted succesfully", 204

class Users(Resource):

    @admin_required
    def get(self):
        users = db.session.query(UserModel).all()
        return jsonify({'Users': [user.to_json() for user in users]})

    @admin_required
    def post(self):
        user = UserModel.from_json(request.get_json())
        emailInUse = db.session.query(UserModel).filter(UserModel.email == user.email).scalar() is not None
        if emailInUse:
            return 'Email already in use', 409
        else:
            db.session.add(user)
            db.session.commit()
            return user.to_json(), 201
