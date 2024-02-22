from logging import DEBUG
from sqlite3 import Connection
from .util.db_functions import get_db

from flask import Flask, g



app: Flask = Flask(__name__, template_folder="templates", static_folder="static")
app.config.from_prefixed_env()
app.logger.setLevel(DEBUG)

from .blueprints.admin import admin
from .blueprints.events import events
from .blueprints.jean_blueprint import jean_blueprint
from .blueprints.login_logout import login_logout
from .blueprints.main import main
from .blueprints.mia_blueprint import mia_blueprint
from .blueprints.misc import misc
from .blueprints.profile import profile
from .blueprints.registration import registration
from .blueprints.clubs_blu import clubs_blu


app.register_blueprint(admin)
app.register_blueprint(events)
app.register_blueprint(jean_blueprint)
app.register_blueprint(login_logout)
app.register_blueprint(main)
app.register_blueprint(mia_blueprint)
app.register_blueprint(misc)
app.register_blueprint(profile)
app.register_blueprint(registration)
app.register_blueprint(clubs_blu)


def initialise_db() -> None:
    """
    Initialises the database with the script in the 'schema.sql' file.
    """

    with app.app_context():
        db: Connection = get_db()

        with app.open_resource("database/schema.sql", "r") as file:
            db.cursor().executescript(file.read())

        db.commit()


@app.teardown_appcontext
def close_connection(_exception) -> None:
    """
    Closes the database connection.
    This function is invoked automatically.
    """

    db: Connection = getattr(g, "_database", None)

    if db is not None:
        db.close()
