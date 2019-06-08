from flask import Blueprint

indexBlp = Blueprint("indexBlp", __name__, url_prefix="/index")

from .views import *
