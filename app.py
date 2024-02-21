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

from application import app, initialise_db_if_not_present

initialise_db_if_not_present()

if __name__ == '__main__':
    app.run()
