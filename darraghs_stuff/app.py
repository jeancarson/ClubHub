from sqlite3 import OperationalError
from application import app, initialise_db
from application import app, initialise_db, query_db
from flask import render_template, session

try:
    initialise_db()
except OperationalError:
    pass


if __name__ == '__main__':
    app.run()

@app.route("/cohome")
def cohome():
    if "user" in session:
        user: str = session["user"]
        return render_template("index.html", header=f"Hello {user}!")
    return render_template("Coordinator/coordinator_dashboard.html", coordinator_name = "John Doe", active_users = 40, pending_users = 3, club_title = "Club 1", club_description = "Description 1")

@app.route("/menview/<status>")
def parview(status):
    if "user" in session:
        user: str = session["user"]
        return render_template("index.html", header=f"Hello {user}!")
    return render_template("Coordinator/view_participants.html", status = status)


@app.route("/participantview/<status>")
def memview(status):
    if "user" in session:
        user: str = session["user"]
        return render_template("index.html", header=f"Hello {user}!")
    return render_template("Coordinator/member_view.html", status = status)

@app.route("/eventview/<timeline>")
def see_events(timeline):
    if "user" in session:
        user: str = session["user"]
        return render_template("index.html", header=f"Hello {user}!")
    return render_template("Coordinator/multi_event_view", timeline = timeline)

@app.route("/singleeventview")
def edit_event():
    if "user" in session:
        user: str = session["user"]
        return render_template("index.html", header=f"Hello {user}!")
    return render_template("Coordinator/single_event_view.html", event_name = 'Event 1', event_date = '2021-10-10', event_time = '10:00', event_location = 'Location 1', event_description = 'Description 1')
