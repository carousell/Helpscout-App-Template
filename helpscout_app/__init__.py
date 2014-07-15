from flask import Flask
from .core import db


def create_app(config_name='config'):
    app = Flask(__name__)
    app.config.from_object(config_name)

    db.init_app(app)

    from .api import api
    app.register_blueprint(api)

    return app
