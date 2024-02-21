"""
The Flask application is run from here.

There are 49 registered users:
- 1 Administrator    (admin)
- 24 Coordinators    (coordinator1, coordinator2, ..., coordinator24)
- 24 Students        (student1, student2, ..., student24)

Password for admin: Admin0
Password for all Coordinators: Coordinator0
Password for all Students: Student0
"""

from application import *


# Only invoke this function after deleting database/database.db
# There seems to be an issue when u call this in debug mode, so um.. don't.
# initialise_db()

if __name__ == '__main__':
    app.run()
