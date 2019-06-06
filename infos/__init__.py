from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from redis import StrictRedis
from flask_session import Session
from config import config


cf = config["Deve"]

# SET FLASK APPLICATION
apply = Flask(__name__)
apply.config.from_object(cf)
# SET FLASK-SQLALCHEMY
db = SQLAlchemy(apply)
# SET REDIS
redis_store = StrictRedis(host=cf.REDIS_HOST, port=cf.REDIS_PORT)
# SET CSRF PROTECT
# response = make_response(body)
# response.set_cookie("key", "value", max)
CSRFProtect(apply)

# SET FLASK-SESSION
# flask_session.Session sets the session saving path
# flask.session sets real session
Session(apply)
