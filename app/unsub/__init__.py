from flask import Blueprint

unsub = Blueprint('unsub', __name__)

from . import views
