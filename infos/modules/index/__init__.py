from flask import Blueprint

indexBlp = Blueprint("indexBlp", __name__)

from .views import *
