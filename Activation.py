# The Main Activation Program
from flask_wtf.csrf import generate_csrf

from infos import InfosFactory, DB as db, models
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


apply = InfosFactory("Deve")()

migrate = Migrate(apply, db)
manager = Manager(apply)
manager.add_command("dbmv", MigrateCommand)


@apply.after_request
def csrf_token_generator(response):
    token = generate_csrf()
    response.set_cookie("csrf_token", token)
    return response


def main():
    """Shell:
    python *.py dbmv init
    python *.py dbmv migrate -m'//version//'
    python *.py dbmv upgrade[downgrade [version]]
    """
    # print(apply.url_map)
    manager.run()


if __name__ == "__main__":
    main()
