from flask import render_template, session, Blueprint, request, flash, redirect, url_for

from ..util import db_functions as dbf
from ..util.coordinator import edit_club_details as ecd

jean_blueprint = Blueprint("jean_blueprint", __name__)
club_id = 1
coordinator_name = "John Doe"


# @jean_blueprint.route("/cohome")
# def cohome():
#     if "user" in session:
#         user: str = session["user"]
#         return render_template("html/misc/default-home.html", header=f"Hello {user}!")
#     # club_id = club_id
#     club_details = dbf.query_db(ecd.get_club_details.format(club_id=club_id))
#     club_name = club_details["club_name"]
#     club_description = club_details["club_description"]
#     number_of_active_users = dbf.query_db(ecd.count_approved_members.format(club_id=club_id))
#     number_of_pending_users = dbf.query_db(ecd.count_pending_members.format(club_id=club_id))

#     # TODO add the for loop thingy to display details of each event.
#     # TODO this is kinda fine for dispaying info I hope
#     # TODO but need to add the functionality to write to the database when save is pressed.
#     # do form 

#     return render_template("html/coordinator/coordinator-dashboard.html", coordinator_name=coordinator_name,
#                            club_id=club_id, active_users=number_of_active_users, pending_users=number_of_pending_users,
#                            club_title=club_name, club_description=club_description)


# @jean_blueprint.route("/cohome", methods=["POST"])
# def save_club_details():
#     club_name = request.form["club_name"]
#     club_description = request.form["club_description"]
#     number_of_active_users = dbf.query_db(ecd.count_approved_members.format(club_id=club_id))
#     number_of_pending_users = dbf.query_db(ecd.count_pending_members.format(club_id=club_id))
#     dbf.modify_db(ecd.save_club_details.format(club_id=club_id, club_name=club_name, club_description=club_description))
#     return render_template("html/coordinator/coordinator-dashboard.html", coordinator_name=coordinator_name,
#                            club_id=club_id, active_users=number_of_active_users, pending_users=number_of_pending_users,
#                            club_title=club_name, club_description=club_description)



from flask import request, render_template

@jean_blueprint.route("/cohome", methods=["GET"])
def cohome():
    if "user" in session:
        user = session["user"]
        return render_template("html/misc/default-home.html", header=f"Hello {user}!")

    club_details = dbf.query_db(ecd.get_club_details.format(club_id=club_id))[0]
    club_name = club_details["club_name"]
    club_description = club_details["club_description"]

    number_of_active_users = dbf.query_db(ecd.count_approved_members.format(club_id=club_id))[0][0]
    number_of_pending_users = dbf.query_db(ecd.count_pending_members.format(club_id=club_id))[0][0]





    limited_upcoming_events = dbf.query_db(ecd.limited_view_all_upcoming_events.format(club_id=club_id, limit =3))
    event_details = []
    if limited_upcoming_events is None:
        limited_upcoming_events = []
    else:
        for event in limited_upcoming_events:
            number_of_approved_participants = dbf.query_db(ecd.count_approved_participants.format(event_id=event["event_id"]))[0][0]
            number_of_pending_participants = dbf.query_db(ecd.count_pending_participants.format(event_id=event["event_id"]))[0][0]
            event_details.append({
                'event_id': event["event_id"],
                'event_name': event["event_name"],
                'event_date': event["date_and_time"],
                'approved_participants': number_of_approved_participants,
                'pending_participants': number_of_pending_participants,
            })




    return render_template("html/coordinator/coordinator-dashboard.html",
                        coordinator_name=coordinator_name,
                        club_id=club_id,
                        active_users=number_of_active_users,
                        pending_users=number_of_pending_users,
                        club_title=club_name,
                        club_description=club_description,
                        limited_events=event_details

                        )

@jean_blueprint.route("/cohome", methods=["POST"])
def save_club_details():
    club_id = request.form["club_id"]
    club_name = request.form["club_name"]
    club_description = request.form["club_description"]

    try:
        # Update the database
        dbf.modify_db(ecd.save_club_details.format(club_id=club_id, new_name=club_name, new_description=club_description))

        # Print a message for debugging
        print("Database updated successfully")

        # Flash a success message
        flash("Club details successfully updated", "success")

    except Exception as e:
        # Print an error message for debugging
        print(f"Error updating database: {e}")

    # Redirect to the /cohome route after processing the form
    return redirect(url_for('jean_blueprint.cohome', club_id=club_id))

#-------------------end of coordinator dashboard--------------------------------------------------------------------------





@jean_blueprint.route("/menview/<status>")
def parview(status):
    if "user" in session:
        user: str = session["user"]
        return render_template("html/misc/default-home.html", header=f"Hello {user}!")

    return render_template("html/coordinator/view-participants.html", status=status)


@jean_blueprint.route("/participantview/<status>")
def memview(status):
    if "user" in session:
        user: str = session["user"]
        return render_template("html/misc/default-home.html", header=f"Hello {user}!")

    return render_template("html/coordinator/member-view.html", status=status)


@jean_blueprint.route("/eventview/<timeline>")
def see_events(timeline):
    if "user" in session:
        user: str = session["user"]
        return render_template("html/misc/default-home.html", header=f"Hello {user}!")

    return render_template("html/coordinator/multi-event-view.html", timeline=timeline)

# ----------------------------Start of single event--------------------------------------------
@jean_blueprint.route("/new-event")
def new_event():
    if "user" in session:
        user: str = session["user"]
        return render_template("html/misc/default-home.html", header=f"Hello {user}!")

    return render_template("html/coordinator/single-event-view.html")

#TODO have this write to database, probably will encounter same problem as before



@jean_blueprint.route("/edit-event/<int:event_id>")
def edit_event(event_id):
    if "user" in session:
        user: str = session["user"]
        return render_template("html/misc/default-home.html", header=f"Hello {user}!")
    event_details = dbf.query_db(ecd.view_single_event.format(event_id=event_id))[0]
    return render_template("html/coordinator/single-event-view.html",  event_name = event_details["event_name"], event_date=event_details["date_and_time"],
                            event_location=event_details["venue"], event_description=event_details["event_description"],)

#---------------------------------------end of single event--------------------------------------------------
#TODO fix build error
# --------------End of Pages functions-----------------

