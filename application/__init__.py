from flask import Flask, g
from sqlite3 import Connection

from .blueprints.main import main
from .blueprints.login_logout import login_logout
from .blueprints.registration import registration
from .blueprints.misc import misc
from .util.database import get_db, query_db


app: Flask = Flask(import_name=__name__)
app.config.from_prefixed_env()

app.register_blueprint(main)
app.register_blueprint(login_logout)
app.register_blueprint(registration)
app.register_blueprint(misc)


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

        with app.open_resource("schema.sql", "r") as file:
            db.cursor().executescript(file.read())

        db.commit()
