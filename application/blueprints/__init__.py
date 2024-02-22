from flask import Blueprint, Flask

from .admin import admin
from .clubs import clubs
from .coordinator import coordinator
from .events import events
from .login_logout import login_logout
from .main import main
from .misc import misc
from .profile import profile
from .registration import registration
from .student import student

all_blueprints: list[Blueprint] = [
    admin, clubs, coordinator, events,
    login_logout, main, misc, profile,
    registration, student
]

def register_all_blueprints(app: Flask) -> None:

    for blueprint in all_blueprints:
        app.register_blueprint(blueprint)
