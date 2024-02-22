from flask import Blueprint, redirect, url_for, request, render_template

from ..util.coordinator import coordinator_functions

coordinator = Blueprint("coordinator", __name__)


# Coordinator dashboard
@coordinator.route("/cohome", methods=["GET"])
def cohome():
    club_id, coordinator_name = coordinator_functions.check_coordinator_session(return_coordinator_info=True)

    # Club details section
    club_name = coordinator_functions.get_club_details(club_id)[0]
    club_description = coordinator_functions.get_club_details(club_id)[1]

    # Member details section
    number_of_active_users = coordinator_functions.count_active_users(club_id)
    number_of_pending_users = coordinator_functions.count_pending_users(club_id)

    # Event details section
    limited_upcoming_events = coordinator_functions.limited_view_all_upcoming_events(club_id)
    event_details = []

    if limited_upcoming_events is None:
        limited_upcoming_events = []

    else:
        for event in limited_upcoming_events:
            number_of_pending_participants = coordinator_functions.count_pending_participants(event["event_id"])
            number_of_approved_participants = coordinator_functions.count_approved_participants(event["event_id"])
            event_details.append(
                {
                    'event_id': event["event_id"],
                    'event_name': event["event_name"],
                    'event_date': event["date"],
                    'approved_participants': number_of_approved_participants,
                    'pending_participants': number_of_pending_participants,
                }
            )

    return render_template(
        "html/coordinator/coordinator-dashboard.html",
        coordinator_name=coordinator_name,
        club_id=club_id,
        active_users=number_of_active_users,
        pending_users=number_of_pending_users,
        club_title=club_name,
        club_description=club_description,
        limited_events=event_details
    )


# To be called when the save button for club details is pressed
@coordinator.route("/cohome", methods=["POST"])
def save_club_details():

    # Get club id from session
    club_id = coordinator_functions.check_coordinator_session()
    club_name = request.form["club_name"]
    club_description = request.form["club_description"]

    coordinator_functions.save_club_details(club_id, club_name, club_description)

    return redirect(
        url_for(
            'coordinator.cohome',
            club_id=club_id
        )
    )


# View members of a certain status
@coordinator.route("/memview/<status>", methods=["GET"])
def view_members(status):
    club_id = coordinator_functions.check_coordinator_session()
    status_users = coordinator_functions.get_all_members(club_id, status)

    return render_template(
        "html/coordinator/member-view.html",
        status=status,
        status_users=status_users
    )


# Save changes to member status
# Note, decided to take status arameter out here, may end up putting it back
@coordinator.route("/memview", methods=["POST"])
def save_member_details():
    club_id = coordinator_functions.check_coordinator_session()

    for user_id in request.form.getlist("user_id"):
        new_validity = str(request.form.get(f"status_{user_id}")).upper()
        print(f"New Validity: {new_validity}")
        coordinator_functions.save_member_status(club_id, user_id, new_validity)
        # Call delete membershere

    coordinator_functions.delete_rejected_members(club_id)

    return redirect(
        url_for('coordinator.cohome', club_id=club_id)
    )


# View participants of a certian status for a specific event
@coordinator.route("/participantview/<status>/<event_id>", methods=["GET"])
def parview(status, event_id):
    # No club_id here? I think it's not needed
    coordinator_functions.check_coordinator_session()
    status_pars = coordinator_functions.get_all_participants(event_id, status)
    event_name = coordinator_functions.get_event_details(event_id)["event_name"]

    return render_template(
        "html/coordinator/view-participants.html",
        status=status,
        event_id=event_id,
        status_pars=status_pars,
        event_name=event_name
    )


# Save changes to participant status and delete rejected participants
# Note, decided to take status arameter out here, may end up putting it back
@coordinator.route("/participantview", methods=["POST"])
def save_participant_details():
    club_id = coordinator_functions.check_coordinator_session()
    event_id = request.form.get("event_id")

    # Loops through every participant in the form
    for user_id in request.form.getlist("user_id"):
        new_validity = str(request.form.get(f"status_{user_id}")).upper()
        coordinator_functions.save_participant_status(event_id=event_id, user_id=user_id, new_validity=new_validity)

    coordinator_functions.delete_rejected_participants(event_id=event_id)

    return redirect(
        url_for('coordinator.cohome', club_id=club_id)
    )


# View all past/upcoming events
@coordinator.route("/eventview/<timeline>")
def see_events(timeline):

    club_id = coordinator_functions.check_coordinator_session()

    timelined_events = coordinator_functions.view_all_events(club_id, timeline)
    event_details = []
    if timelined_events is None:
        timelined_events = []

    else:
        for event in timelined_events:
            number_of_pending_participants = coordinator_functions.count_pending_participants(event["event_id"])
            number_of_approved_participants = coordinator_functions.count_approved_participants(event["event_id"])
            event_details.append(
                {
                    'event_id': event["event_id"],
                    'event_name': event["event_name"],
                    'event_date': event["date"],
                    'approved_participants': number_of_approved_participants,
                    'pending_participants': number_of_pending_participants,
                }
            )

    return render_template(
        "html/coordinator/multi-event-view.html",
        timeline=timeline,
        timelined_events=event_details
    )


# Submitting a new single event, blank form
@coordinator.route("/new-event")
def new_event():

    club_id = coordinator_functions.check_coordinator_session()

    return render_template("html/coordinator/single-event-view.html")


# Write a new entry to database
@coordinator.route("/new-event", methods=["POST"])
def add_event():

    club_id = coordinator_functions.check_coordinator_session()
    event_name = request.form["name"]
    event_date = request.form["date"]
    event_time = request.form["time"]
    event_location = request.form["venue"]
    event_description = request.form["description"]

    coordinator_functions.add_event(
        event_name=event_name,
        event_date=event_date,
        event_time=event_time,
        event_location=event_location,
        event_description=event_description,
        club_id=club_id
    )

    return redirect(
        url_for('coordinator.cohome', club_id=club_id)
    )


# Editing an existing event - populate form with existing details
@coordinator.route("/edit-event/<int:event_id>")
def edit_event(event_id):

    event_details = coordinator_functions.get_event_details(event_id)

    return render_template(
        "html/coordinator/single-event-view.html",
        event_id=event_id,
        event_name=event_details["event_name"],
        event_date=event_details["date"],
        event_time=event_details["time"],
        event_location=event_details["venue"],
        event_description=event_details["event_description"]
    )


# Perform an update on the database to change the event details
@coordinator.route("/edit-event/<int:event_id>", methods=["POST"])
def update_event(event_id):

    club_id = coordinator_functions.check_coordinator_session()
    event_name = request.form["name"]
    event_date = request.form["date"]
    event_time = request.form["time"]
    event_location = request.form["venue"]
    event_description = request.form["description"]

    coordinator_functions.update_event(
        event_id,
        event_name,
        event_description,
        event_date,
        event_time,
        event_location
    )

    return redirect(
        url_for('coordinator.cohome', club_id=club_id)
    )
