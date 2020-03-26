import flask

from app import config


the_app = flask.Flask(__name__)
the_app.config.from_object(config.Config)


from app import routes
