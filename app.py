"""
The Flask application is run from here.

There are 19 registered users:
- 1 Administrator   (admin)
- 9 Coordinators    (coordinator-1, coordinator-2, ..., coordinator-9)
- 9 Students        (student-1, student-2, ..., student-9)

Password for admin: Admin0
Password for all Coordinators: Coordinator0
Password for all Students: Student0
"""

from sqlite3 import OperationalError
from application import app, initialise_db


try:
    initialise_db()
except OperationalError:
    pass

if __name__ == '__main__':
    app.run()
