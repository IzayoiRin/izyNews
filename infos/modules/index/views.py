from flask import session
from . import indexBlp
from Activation import factory

redis_db = factory("redis")


@indexBlp.route('/', methods=['GET', 'POST'])
def index():
    # set session and saving to redis though flask_session
    session["key"] = 123
    return "Hello world"
