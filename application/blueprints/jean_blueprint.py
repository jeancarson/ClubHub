from flask import render_template, session, Blueprint


jean_blueprint = Blueprint("jean_blueprint", __name__)


@jean_blueprint.route("/cohome")
def cohome():
    if "user" in session:
        user: str = session["user"]
        return render_template("html/index.html", header=f"Hello {user}!")

    return render_template("html/Coordinator/coordinator_dashboard.html", coordinator_name = "John Doe", active_users = 40, pending_users = 3, club_title = "Club 1", club_description = "Description 1")


@jean_blueprint.route("/menview/<status>")
def parview(status):
    if "user" in session:
        user: str = session["user"]
        return render_template("html/index.html", header=f"Hello {user}!")

    return render_template("html/Coordinator/view_participants.html", status = status)


@jean_blueprint.route("/participantview/<status>")
def memview(status):
    if "user" in session:
        user: str = session["user"]
        return render_template("html/index.html", header=f"Hello {user}!")
    return render_template("html/Coordinator/member_view.html", status = status)


@jean_blueprint.route("/eventview/<timeline>")
def see_events(timeline):
    if "user" in session:
        user: str = session["user"]
        return render_template("html/index.html", header=f"Hello {user}!")
    return render_template("html/Coordinator/multi_event_view.html", timeline = timeline)


@jean_blueprint.route("/singleeventview")
def edit_event():
    if "user" in session:
        user: str = session["user"]
        return render_template("html/index.html", header=f"Hello {user}!")
    return render_template("html/Coordinator/single_event_view.html", event_name = 'Event 1', event_date = '2021-10-10', event_time = '10:00', event_location = 'Location 1', event_description = 'Description 1')
