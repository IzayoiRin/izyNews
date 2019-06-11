# The Main Activation Program
from infos import InfosFactory, DB as db, models
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


factory = InfosFactory("Deve")
apply= factory()

migrate = Migrate(apply, db)
manager = Manager(apply)
manager.add_command("dbmv", MigrateCommand)


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
