# create
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from redis import StrictRedis
from flask_session import Session
from config import AppConfig as Cf
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


# SET FLASK APPLICATION
apply = Flask(__name__)
apply.config.from_object(Cf)
# SET FLASK-SQLALCHEMY
db = SQLAlchemy(apply)
# SET REDIS
redis_store = StrictRedis(host=Cf.REDIS_HOST, port=Cf.REDIS_PORT)
# SET CSRF PROTECT
# response = make_response(body)
# response.set_cookie("key", "value", max)
CSRFProtect(apply)

# SET FLASK-SESSION
# flask_session.Session sets the session saving path
# flask.session sets real session
Session(apply)

migrate = Migrate(apply, db)
manager = Manager(apply)
manager.add_command("dbmv", MigrateCommand)

# apply.register_blueprint(blp)


@apply.route('/', methods=['GET', 'POST'])
def index():
    # set session and saving to redis though flask_session
    session["key"] = 123
    return "Hello world"


def main():
    """Shell:
    python *.py dbmv init
    python *.py dbmv migrate -m'//version//'
    python *.py dbmv upgrade[downgrade [version]]
    """
    manager.run()


if __name__ == "__main__":
    main()


