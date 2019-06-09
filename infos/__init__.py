import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from redis import StrictRedis
from flask_session import Session
from config import config


__all__ = []


class InfosFactory(object):

    DB = None  # type: SQLAlchemy
    REDIS = None  # type: StrictRedis
    
    def __init__(self, cf, apply=None):
        cf = config[cf]
        # SET LOGGING CONFIG
        self._logging(cf)
        # SET FLASK APPLICATION
        if apply is None:
            self.apply = Flask(__name__)
        if self._app_init(cf):
            # SET FLASK-SQLALCHEMY
            self.DB = SQLAlchemy(self.apply)
            # SET REDIS
            self.REDIS = StrictRedis(host=cf.REDIS_HOST, port=cf.REDIS_PORT, decode_responses=cf.REDIS_DECODE)
            # SET CSRF PROTECT
            # response = make_response(body)
            # response.set_cookie("key", "value", max)
            CSRFProtect(apply)
            # SET FLASK-SESSION
            # flask_session.Session sets the session saving path
            # flask.session sets real session
            Session(apply)
            # BLUEPRINT REGISTER
            self._load_blps()

    def _logging(self, cf):
        logging.basicConfig(level=cf.LOG_LEVEL)
        file_log_handler = RotatingFileHandler("runLogs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
        formatter = logging.Formatter("%(levelname)s-%(filename)s:%(lineno)d-%(message)s")
        file_log_handler.setFormatter(formatter)
        logging.getLogger().addHandler(file_log_handler)

    def _app_init(self, cf):
        try:
            self.apply.config.from_object(cf)
        except Exception as e:
            logging.error("Application Initiation Failed")
            return 
        else:
            return 1

    def _load_blps(self):
        from .modules import BLPS
        for blp in BLPS:
            self.apply.register_blueprint(blp)

    def __call__(self, arg="app"):
        assert isinstance(self.DB, SQLAlchemy) and isinstance(self.REDIS, StrictRedis), "Config Loading Failed"
        dic = {"app": self.apply, "db": self.DB, "redis": self.REDIS}
        return dic[arg]
