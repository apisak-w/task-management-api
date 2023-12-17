from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
from app.extensions import db

def create_app(config_class=Config):
  app = Flask(__name__)
  app.config.from_object(config_class)
  
  db.init_app(app)
  
  from app.task import bp as tasks_bp
  app.register_blueprint(tasks_bp, url_prefix='/tasks')
  
  return app