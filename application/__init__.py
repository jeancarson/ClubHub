from sqlite3 import Connection
from logging import INFO, DEBUG

from flask import Flask, g

from .blueprints.jean_blueprint import jean_blueprint
from .blueprints.login_logout import login_logout
from .blueprints.main import main
from .blueprints.admin import admin
from .blueprints.mia_blueprint import mia_blueprint
from .blueprints.misc import misc
from .blueprints.registration import registration
from .blueprints.profile import profile
from .util.db_functions import get_db

app: Flask = Flask(import_name=__name__, template_folder="templates", static_folder="static")
app.config.from_prefixed_env()
app.logger.setLevel(DEBUG)

app.register_blueprint(main)
app.register_blueprint(login_logout)
app.register_blueprint(registration)
app.register_blueprint(profile)
app.register_blueprint(misc)
app.register_blueprint(admin)
app.register_blueprint(jean_blueprint)


@app.teardown_appcontext
def close_connection(_exception) -> None:
    """
    Closes the database connection.
    This function is invoked automatically.
    """

    db: Connection = getattr(g, "_database", None)

    if db is not None:
        db.close()


def initialise_db() -> None:
    """
    Initialises the database with the script in the 'schema.sql' file.
    """

    with app.app_context():
        db: Connection = get_db()

        with app.open_resource("database/schema.sql", "r") as file:
            db.cursor().executescript(file.read())

        db.commit()
