# The Main Activation Program
from infos import InfosFactory
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


factory = InfosFactory("Deve")
apply, db = factory(), factory("db")

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
