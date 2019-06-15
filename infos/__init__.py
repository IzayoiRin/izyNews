import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from redis import StrictRedis
from flask_session import Session
from config import conf


class InitialError(Exception):
    pass


DB = SQLAlchemy()
REDIS = None  # type: StrictRedis


class InfosFactory(object):

    def __init__(self, cf_tag, apply=None):

        cf = conf[cf_tag]
        # SET LOGGING CONFIG
        self._logging(cf)
        # SET FLASK APPLICATION
        if apply is None:
            self.apply = Flask(__name__)
        else:
            self.apply = apply
        # LOAD CONFIG
        self._app_init(cf)
        # SET FLASK-SQLALCHEMY
        DB.init_app(self.apply)
        # SET REDIS
        global REDIS
        REDIS = StrictRedis(host=cf.REDIS_HOST, port=cf.REDIS_PORT, decode_responses=cf.REDIS_DECODE)
        # SET CSRF PROTECT
        # response = make_response(body)
        # response.set_cookie("key", "value", max)
        # CSRFProtect(self.apply)
        # SET FLASK-SESSION
        # flask_session.Session sets the session saving path
        # flask.session sets real session
        Session(self.apply)
        # BLUEPRINT REGISTER
        self._load_blps()

    def _logging(self, cf):
        # SET LOGGER
        # logger = logging.getLogger()
        # stream_log_handler = logging.StreamHandler()
        # SET PRINT LEVEL: higher than cf.LOG_LEVEL
        # stream_log_handler.setLevel(logging.INFO)
        # LOGGER LOAD HANDLER
        # logger.addHandler(stream_log_handler)
        # SET HANDLER
        file_log_handler = RotatingFileHandler("runLogs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
        # SERT RECORD LEVEL
        file_log_handler.setLevel(cf.LOG_LEVEL)
        # SET FORMATTER
        formatter = logging.Formatter(
            "%(levelname)s: *%(asctime)s* %(name)s@%(filename)s=%(funcName)s=:%(lineno)d=%(message)s"
        )
        # SET RECORD FORMAT
        file_log_handler.setFormatter(formatter)
        # LOGGER LOAD HANDLER
        logging.getLogger().addHandler(file_log_handler)

    def _app_init(self, cf):
        try:
            self.apply.config.from_object(cf)
        except Exception as e:
            logging.critical("App Initial: {}".format(e))
            raise InitialError("Application Initiation Failed")

    def _load_blps(self):
        from .modules import BLPS
        for blp in BLPS:
            self.apply.register_blueprint(blp)

    def __call__(self):
        assert isinstance(REDIS, StrictRedis), "Config Loading Failed"
        return self.apply
