import logging

from redis import StrictRedis


class BaseConfig(object):
    # flask application config
    SECRET_KEY = "123456"

    # SQLAlchemy config
    SQLALCHEMY_DATABASE_URI = "mysql://root:asdlllasd@127.0.0.1:3306/news_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Redis config
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379
    REDIS_DECODE = True

    # SESSION_TYPE [redis, filesystem, sqlalchemy, memcached, mongdb]
    SESSION_TYPE = "redis"

    # INIT REDIS OR SET SAVING REDIS OBJECT
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    # DEFAULT PREFIX IS "session:"
    SESSION_KEY_PREFIX = "session:"
    # MAKE SESSION SIGNED THEN SAVE TO REDIS
    SESSION_USE_SIGNER = True
    # SET SESSION LIFE TIME
    SESSION_PERMANENT = True
    # SET THE MAX LIFE TIME OF SESSION (/s)
    PERMANENT_SESSION_LIFETIME = 60 * 10


class AppConfig(BaseConfig):

    DEBUG = True
    LOG_LEVEL = logging.WARNING


class ProductConfig(BaseConfig):

    LOG_LEVEL = logging.WARNING


class TestConfig(BaseConfig):

    DEBUG = True
    LOG_LEVEL = logging.INFO


conf = {"Deve": AppConfig, "Prod": ProductConfig, "Test": TestConfig}