from flask import render_template, session, Blueprint, request
import application.util.db_functions as dbf
import application.util.Coordinator.edit_club_details as ecd


jean_blueprint = Blueprint("jean_blueprint", __name__)
club_id = 6
coordinator_name = "John Doe"



@jean_blueprint.route("/cohome")
def cohome():
    if "user" in session:
        user: str = session["user"]
        return render_template("html/index.html", header=f"Hello {user}!")
    # club_id = club_id
    club_details = dbf.query_db(ecd.get_club_details.format(club_id=club_id))
    club_name = club_details["club_name"]
    club_description = club_details["club_description"]
    number_of_active_users = dbf.query_db(ecd.count_approved_members.format(club_id=club_id))
    number_of_pending_users = dbf.query_db(ecd.count_pending_members.format(club_id=club_id))
    #TODO add the for loop thingy to display details of each event.
    #TODO this is kinda fine for dispaying info I hope... but need to add the functionality to write to the database when save is pressed.
    return render_template("html/Coordinator/coordinator_dashboard.html", coordinator_name=coordinator_name, club_id = club_id, active_users=number_of_active_users, pending_users=number_of_pending_users, club_title = club_name, club_description = club_description)

@jean_blueprint.route("/cohome", methods=["POST"])
def save_club_details():
    club_name = request.form["club_name"]
    club_description = request.form["club_description"]
    number_of_active_users = dbf.query_db(ecd.count_approved_members.format(club_id=club_id))
    number_of_pending_users = dbf.query_db(ecd.count_pending_members.format(club_id=club_id))
    dbf.modify_db(ecd.save_club_details.format(club_id=club_id, club_name=club_name, club_description=club_description))
    return render_template("html/Coordinator/coordinator_dashboard.html", coordinator_name=coordinator_name, club_id = club_id, active_users=number_of_active_users, pending_users=number_of_pending_users, club_title = club_name, club_description = club_description)


def display_event_details():
    limited_upcoming_events = dbf.query_db(ecd.limited_view_all_upcoming_events.format(club_id=club_id))
    for event in limited_upcoming_events:
        number_of_approved_participants = dbf.query_db(ecd.count_approved_participants.format(event_id=event["event_id"]))
        number_of_pending_participants = dbf.query_db(ecd.count_pending_participants.format(event_id=event["event_id"]))
        return render_template("html/Coordinator/coordinator_dashboard.html", coordinator_name=coordinator_name, club_id = club_id, club_title = "Club 1", club_description = "Description 1", upcoming_events=limited_upcoming_events, approved_participants=number_of_approved_participants, pending_participants=number_of_pending_participants)

@jean_blueprint.route("/menview/<status>")
def parview(status):
    if "user" in session:
        user: str = session["user"]
        return render_template("html/index.html", header=f"Hello {user}!")

    return render_template("html/Coordinator/view_participants.html", status=status)


@jean_blueprint.route("/participantview/<status>")
def memview(status):
    if "user" in session:
        user: str = session["user"]
        return render_template("html/index.html", header=f"Hello {user}!")

    return render_template("html/Coordinator/member_view.html", status=status)


@jean_blueprint.route("/eventview/<timeline>")
def see_events(timeline):
    if "user" in session:
        user: str = session["user"]
        return render_template("html/index.html", header=f"Hello {user}!")

    return render_template("html/Coordinator/multi_event_view.html", timeline=timeline)


@jean_blueprint.route("/singleeventview")
def edit_event():
    if "user" in session:
        user: str = session["user"]
        return render_template("html/index.html", header=f"Hello {user}!")

    return render_template("html/Coordinator/single_event_view.html", event_name='Event 1', event_date='2021-10-10',
                           event_time='10:00', event_location='Location 1', event_description='Description 1')

# --------------End of Pages functions-----------------

# @jean_blueprint.route("/cohome", methods=["POST"])
# def save_club_details(club_id, club_name, club_description):
#     dbf.modify_db(ecd.save_club_details.format(club_id=club_id, club_name=club_name, club_description=club_description))
#     return render_template("html/Coordinator/coordinator_dashboard.html", coordinator_name=coordinator_name, club_id = club_id, club_title = club_name, club_description = club_description)
#

