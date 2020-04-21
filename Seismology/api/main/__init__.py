import os
from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy


api = Api()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    load_dotenv()
    if not os.path.exists(os.getenv('SQLALCHEMY_DATABASE_PATH') + os.getenv('SQLALCHEMY_DATABASE_NAME')):
	       os.mknod(os.getenv('SQLALCHEMY_DATABASE_PATH') + os.getenv('SQLALCHEMY_DATABASE_NAME'))
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.getenv('SQLALCHEMY_DATABASE_PATH') + os.getenv('SQLALCHEMY_DATABASE_NAME')
    db.init_app(app)

    if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
        def activatePrimaryKeys(conection, conection_record):
            conection.execute('pragma foreign_keys=ON')
        with app.app_context():
            from sqlalchemy import event
            event.listen(db.engine, 'connect', activatePrimaryKeys)

    import main.resources as resources
    api.add_resource(resources.SensorsResource, '/sensors')
    api.add_resource(resources.SensorResource, '/sensor/<id>')
    api.add_resource(resources.UnverifiedSeismsResource, '/unverified-seisms')
    api.add_resource(resources.UnverifiedSeismResource, '/unverified-seism/<id>')
    api.add_resource(resources.VerifiedSeismsResource, '/verified-seisms')
    api.add_resource(resources.VerifiedSeismResource, '/verified-seism/<id>')
    api.add_resource(resources.UsersResource, '/users')
    api.add_resource(resources.UserResource, '/user/<id>')
    api.init_app(app)
    return app
