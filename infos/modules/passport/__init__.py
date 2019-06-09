from flask import Blueprint

passportBlp = Blueprint("passportBlp", __name__, url_prefix="/passport")

from .views import *
