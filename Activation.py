# The Main Activation Program
from flask import session
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from infos import apply, db, redis_store

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