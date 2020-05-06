from flask import request, jsonify, Blueprint
from .. import db
from main.models import UserModel, SensorModel
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from main.mail.functions import sendMail


auth = Blueprint('auth', __name__, url_prefix = '/auth')

@auth.route('/login', methods = ['POST'])
def login():
    user = db.session.query(UserModel).filter(UserModel.email == request.get_json().get("email")).first_or_404()
    if user.validate_password(request.get_json().get("password")):
        token = create_access_token(identity = user)
        data = '{"id":"' + str(user.id) + '","email":"' + str(user.email) + '", "access_token":"' + token + '"}'
        return data, 200
    else:
        return "Incorrect password", 401


@auth.route('/checksensors', methods = ['GET'])
def checkStatus():
    sensors = db.session.query(SensorModel).filter(SensorModel.active == True).filter(SensorModel.status == False).all()
    if sensors:
        admins = db.session.query(UserModel).filter(UserModel.admin == True).all()
        if admins:
            adminList = [admin.email for admin in admins]
            sendMail(adminList, "Deactivated sensors", "mail/sensor", sensorList = sensors)
        return jsonify({ 'sensors': [sensor.to_json() for sensor in sensors]})
    else:
        return "There're no deactivated sensors", 200
