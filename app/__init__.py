from flask import Flask

from app.extensions import init_extensions
from app.models.task import *
from app.models.task_action_logs import *

from config import Config

def create_app(config_class=Config):
  app = Flask(__name__)
  app.config.from_object(config_class)
  app.app_context().push()
  
  init_extensions(app)
  
  db.create_all()
  
  from app.task import bp as tasks_bp
  app.register_blueprint(tasks_bp, url_prefix='/tasks')
  
  return app