from sqlite3 import OperationalError

from application import app, initialise_db

try:
    initialise_db()
except OperationalError:
    pass

if __name__ == '__main__':
    app.run()
