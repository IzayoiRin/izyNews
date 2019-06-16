from flask import Blueprint

detailBlp = Blueprint("detailBlp", __name__, url_prefix="/detail")

from .views import *
