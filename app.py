from sqlite3 import OperationalError

from application import app, initialise_db


try:
    initialise_db()
except OperationalError:
    pass


# DARRAGH – TODO: Fix styles overriding each other and add navbar to admin pages


if __name__ == '__main__':
    app.run()
