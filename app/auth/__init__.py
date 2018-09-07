from flask import Blueprint
from . import views,forms

auth = Blueprint('auth',__name__)

from . import views


def create_app(config_name):
    #...
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix = '/auth')