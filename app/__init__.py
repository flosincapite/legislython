import flask
import flask_socketio

from app import config


the_app = flask.Flask(__name__)
the_app.config.from_object(config.Config)
socketio = flask_socketio.SocketIO(the_app)


from app import routes
