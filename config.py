from redis import StrictRedis


class AppConfig(object):
    # flask application config
    DEBUG = True
    SECRET_KEY = "123456"

    # SQLAlchemy config
    SQLALCHEMY_DATABASE_URI = "mysql://root:asdlllasd@localhost/news"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Redis config
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    # SESSION_TYPE [redis, filesystem, sqlalchemy, memcached, mongdb]
    SESSION_TYPE = "redis"

    # INIT REDIS OR SET SAVING REDIS OBJECT
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    # DEFAULT PREFIX IS "session:"
    SESSION_PERFIX = "session:"
    # MAKE SESSION SIGNED THEN SAVE TO REDIS
    SESSION_USE_SIGNER = True
    # SET SESSION LIFE TIME
    SESSION_PERMANENT = False
    # SET THE MAX LIFE TIME OF SESSION (/s)
    PERMANENT_SESSION_LIFETIME = 60 * 10

