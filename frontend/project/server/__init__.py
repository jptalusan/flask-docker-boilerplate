import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect

bootstrap = Bootstrap()
socketio = SocketIO()

def create_app(script_info=None):
  app = Flask(
      __name__,
      template_folder='../client/templates',
      static_folder='../client/static'
  )

  app_settings = os.getenv('APP_SETTINGS')
  app.config.from_object(app_settings)

  bootstrap.init_app(app)
  socketio.init_app(app)
  CORS(app)
  csrf = CSRFProtect(app)

  from project.server.main.views import main_blueprint
  app.register_blueprint(main_blueprint, url_prefix='/')

  #app.shell_context_processor({'app': app})

  return app
