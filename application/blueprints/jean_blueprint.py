from flask import render_template, session, Blueprint, request, flash, redirect, url_for

from ..util import db_functions as dbf
from ..util.coordinator import coordinator_functions as cf

import logging

jean_blueprint = Blueprint("jean_blueprint", __name__)



from flask import request, render_template

#-------------------Start of coordinator dashboard--------------------------------------------------------------------------
#***********************************************************
#***********************************************************
#coordinator dashboard
@jean_blueprint.route("/cohome", methods=["GET"])
def cohome():
    club_id, coordinator_name = cf.check_coordinator_session(return_coordinator_info = True)

    #***********************************************************
    #club detailse section
    club_name = cf.get_club_details(club_id)[0]
    club_description = cf.get_club_details(club_id)[1]
    #***********************************************************
    #member details section

    number_of_active_users = cf.count_active_users(club_id)
    number_of_pending_users = cf.count_pending_users(club_id)

    #***********************************************************
    #event details section
    limited_upcoming_events = cf.limited_view_all_upcoming_events(club_id)
    event_details = []
    if limited_upcoming_events is None:
        limited_upcoming_events = []
    else:
        for event in limited_upcoming_events:
            number_of_pending_participants = cf.count_pending_participants(event["event_id"])
            number_of_approved_participants = cf.count_approved_participants(event["event_id"])
            event_details.append({
                'event_id': event["event_id"],
                'event_name': event["event_name"],
                'event_date': event["date"],
                'approved_participants': number_of_approved_participants,
                'pending_participants': number_of_pending_participants,
            })


    #***********************************************************

    return render_template("html/coordinator/coordinator-dashboard.html",
                        coordinator_name=coordinator_name,
                        club_id=club_id,
                        active_users=number_of_active_users,
                        pending_users=number_of_pending_users,
                        club_title=club_name,
                        club_description=club_description,
                        limited_events=event_details
                                                              )

#***********************************************************
#***********************************************************

#to be called when the save button for club details is pressed
@jean_blueprint.route("/cohome", methods=["POST"])
def save_club_details():
    #get club id from session
    club_id = cf.check_coordinator_session()
    club_name = request.form["club_name"]
    club_description = request.form["club_description"]
    cf.save_club_details(club_id, club_name, club_description)
    return redirect(url_for('jean_blueprint.cohome', club_id=club_id))
#***********************************************************
#-------------------end of coordinator dashboard--------------------------------------------------------------------------



#--------------------member_view-----------------------------


#view members of a certain status
@jean_blueprint.route("/memview/<status>", methods=["GET"])
def view_members(status):
    club_id = cf.check_coordinator_session()
    status_users = cf.get_all_members(club_id, status)
    return render_template("html/coordinator/member-view.html", status = status, status_users = status_users)

#save changes to member status
@jean_blueprint.route("/memview", methods=["POST"])
#Note, decided to take status arameter out here, may end up putting it back
def save_member_details():
    club_id = cf.check_coordinator_session()
    for user_id in request.form.getlist("user_id"):
        new_validity = str(request.form.get(f"status_{user_id}")).upper()
        print(f"New Validity: {new_validity}")
        cf.save_member_status(club_id, user_id, new_validity)
        #call delete membershere
    cf.delete_rejected_members(club_id)

    return redirect(url_for('jean_blueprint.cohome', club_id=club_id))





#-----------------------------------------end of member view-----------------------------------------
#---------------------------------------start of participant stuff---------------------------------
#view participants of a certian status for a specific event
@jean_blueprint.route("/participantview/<status>/<event_id>", methods=["GET"])
def parview(status, event_id):
#no club_id here? I think it's not needed
    cf.check_coordinator_session()
    status_pars = cf.get_all_participants(event_id, status)
    event_name = cf.get_event_details(event_id)["event_name"]
    return render_template("html/coordinator/view-participants.html", status=status, event_id=event_id, status_pars = status_pars, event_name = event_name)

#save changes to participant status and delete rejected participants
@jean_blueprint.route("/participantview", methods=["POST"])
#Note, decided to take status arameter out here, may end up putting it back
def save_participant_details():
    club_id = cf.check_coordinator_session()
    event_id = request.form.get("event_id")
    #loops through every participant in the form
    for user_id in request.form.getlist("user_id"):
        new_validity = str(request.form.get(f"status_{user_id}")).upper()
        cf.save_participant_status(event_id = event_id, user_id = user_id, new_validity = new_validity)
    cf.delete_rejected_participants(event_id = event_id)

    return redirect(url_for('jean_blueprint.cohome', club_id= club_id))






#---------------------------------------end of participant stuff-----------------------------------
#view all past/upcoming events
@jean_blueprint.route("/eventview/<timeline>")
def see_events(timeline):
    club_id = cf.check_coordinator_session()

    timelined_events = cf.view_all_events(club_id, timeline)
    event_details = []
    if timelined_events is None:
        timelined_events = []
    else:
        for event in timelined_events:
            number_of_pending_participants = cf.count_pending_participants(event["event_id"])
            number_of_approved_participants = cf.count_approved_participants(event["event_id"])
            event_details.append({
                'event_id': event["event_id"],
                'event_name': event["event_name"],
                'event_date': event["date"],
                'approved_participants': number_of_approved_participants,
                'pending_participants': number_of_pending_participants,
            })
    return render_template("html/coordinator/multi-event-view.html", timeline=timeline, timelined_events=event_details)

# ----------------------------Start of single event--------------------------------------------
#submitting a new single event, blank form
@jean_blueprint.route("/new-event")
def new_event():
    club_id = cf.check_coordinator_session()

    return render_template("html/coordinator/single-event-view.html")

#write a new entry to database
@jean_blueprint.route("/new-event", methods=["POST"])
def add_event():
    club_id = cf.check_coordinator_session()
    event_name = request.form["name"]
    event_date = request.form["date"]
    event_time = request.form["time"]
    event_location = request.form["venue"]
    event_description = request.form["description"]

    cf.add_event(event_name=event_name, event_date=event_date, event_time=event_time, event_location=event_location, event_description=event_description, club_id=club_id)

    return redirect(url_for('jean_blueprint.cohome', club_id=club_id))


#editing an existing event - populate form with existing details
@jean_blueprint.route("/edit-event/<int:event_id>")
def edit_event(event_id):
    event_details = cf.get_event_details(event_id)
    return render_template("html/coordinator/single-event-view.html",event_id = event_id,  event_name = event_details["event_name"], event_date=event_details["date"],event_time=event_details["time"],
                            event_location=event_details["venue"], event_description=event_details["event_description"],)

#perform an update on the database to change the event details
@jean_blueprint.route("/edit-event/<int:event_id>", methods=["POST"])
def update_event(event_id):
    club_id = cf.check_coordinator_session()
    event_name = request.form["name"]
    event_date = request.form["date"]
    event_time = request.form["time"]
    event_location = request.form["venue"]
    event_description = request.form["description"]
    cf.update_event(event_id, event_name,event_description, event_date, event_time, event_location, )
    return redirect(url_for('jean_blueprint.cohome', club_id=club_id))




#---------------------------------------end of single event--------------------------------------------------
# --------------End of Pages functions-----------------
