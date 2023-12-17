from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from flask_restx import Api

db = SQLAlchemy()
api = Api()
swagger = Swagger()

def init_extensions(app):
    db.init_app(app)
    swagger.init_app(app)