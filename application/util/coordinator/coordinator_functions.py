
#These functions are used to handle the coordinator's requests and to interact with the database.


from flask import redirect, url_for, flash, session, Response
import application.util.db_functions as dbf


#-------checking user type and session----------------------
def check_coordinator_session(return_coordinator_info=False):
    user_type = session.get("user-type")
    
    if user_type != "COORDINATOR":
        return redirect("/home")
    
    coordinator_ID = session.get("user-id")

    if coordinator_ID is None:
        # Handle the case where the user is not logged in
        return redirect("/login")
    
    club_id = get_club_id(coordinator_ID)
    coordinator_name =get_coordinator_name(club_id)
#if we want both the club_id and the coordinator_name
    if return_coordinator_info:
        return club_id, coordinator_name
    #if we only want the club_id (allows us to call and assign to a variable without specifying an index)
    else:
        return club_id



#######################################################################################

#Header setup
def get_coordinator_name(club_id):
    coordinator_info = dbf.query_db("""
    select u.first_name, u.last_name
    from users u join clubs c on u.user_id = c.creator
    where c.club_id = {club_id};
    """.format(club_id=club_id))
    if coordinator_info:
        return f"{coordinator_info[0]['first_name']} {coordinator_info[0]['last_name']}"
    else:
        return "Coordinator not found"

def get_club_id(coordinator_id):
    return dbf.query_db("""
    select club_id
    from clubs
    where creator = {coordinator_id};
    """.format(coordinator_id=coordinator_id))[0][0]

#-------viewing and editing club details----------------------

def get_club_details(club_id):
    club_details = dbf.query_db("""
    select *
    from clubs
    where club_id = {club_id};
    """.format(club_id=club_id))[0]
    club_name = club_details["club_name"]
    club_description = club_details["club_description"]
    return club_name, club_description

def save_club_details(club_id: int, new_name: str, new_description: str) -> Response:

    dbf.modify_db(
        """
            UPDATE clubs
            SET
                club_name=?,
                club_description=?
            WHERE club_id=?;
        """,
        new_name,
        new_description,
        club_id
    )

    flash("Club details successfully updated", "info")

    return redirect(url_for('coordinator.cohome', club_id=club_id))



#-------viewing members and participants----------------------
def count_active_users(club_id):
    number_of_active_users = dbf.query_db("""
    select count(user_id)
    from club_memberships
    where club_id ={club_id} and validity = 'APPROVED'
    """.format(club_id=club_id))[0][0]
    return number_of_active_users

def count_pending_users(club_id):
    number_of_pending_users = dbf.query_db("""
    select count(user_id)
    from club_memberships
    where club_id ={club_id} and validity = 'PENDING'
    """.format(club_id=club_id))[0][0]
    return number_of_pending_users

#to get a list of all members of a certain status (approved/pending)
def get_all_members(club_id, status):
    status_users = dbf.query_db( """
    select users.*
    from users join club_memberships on users.user_id = club_memberships.user_id
    where club_memberships.validity = '{status}' and club_memberships.club_id = {club_id};
    """.format(status=status.upper(), club_id = club_id))
    return status_users

#save members after changing their status
def save_member_status(club_id, user_id, new_validity):
    dbf.modify_db("""
    update club_memberships
    set validity = '{NEW_VALIDITY}'
    where user_id = {user_id} and club_id = {club_id}
    """.format(user_id=user_id, club_id=club_id, NEW_VALIDITY=new_validity.upper()))
#This will be run immediately after the save_member_status function, to get rid of the rejected members
def delete_rejected_members(club_id):
    dbf.modify_db("""
    delete 
    from club_memberships
    where validity = 'Rejected' and club_id = {club_id};
    """.format(club_id=club_id))

#-------viewing events----------------------
    #view a small number of events straight on the dashboard
def limited_view_all_upcoming_events(club_id):
    from datetime import datetime

    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return dbf.query_db("""
        SELECT *
        FROM events
        WHERE club_id = {club_id} AND datetime(date || ' ' || time) >= CURRENT_TIMESTAMP
        ORDER BY date
        LIMIT {limit};
    """.format(club_id=club_id, current_date=current_date, limit=5))

def count_pending_participants(event_id):
    return (dbf.query_db("""
    select count(user_id)
    from event_participants
    where event_id ={event_id} and validity = 'PENDING'
    """.format(event_id=event_id))[0][0])

def count_approved_participants(event_id):
    return (dbf.query_db("""
    select count(user_id)
    from event_participants
    where event_id ={event_id} and validity = 'APPROVED'
    """ .format(event_id=event_id))[0][0])
#retreive all participants for a particular event, who are of a certain status
def get_all_participants(event_id, status):
    return (dbf.query_db("""
    select users.*
    from users join event_participants on users.user_id = event_participants.user_id 
    where event_participants.validity = '{status}' and event_participants.event_id = {event_id};
    """.format(status=status.upper(), event_id = event_id)))
#similarly to the save members functon, this function will save the status of the participants after it has been changed
#deleting the rejected participants will be done immediately after this function
def save_participant_status(event_id, user_id, new_validity):
    dbf.modify_db("""
    update event_participants
    set validity = '{NEW_VALIDITY}', updated = CURRENT_TIMESTAMP
    where user_id = {user_id} and event_id = {event_id};
    """.format(user_id=user_id, event_id=event_id, NEW_VALIDITY=new_validity.upper()))

def delete_rejected_participants(event_id):
    dbf.modify_db("""
    delete 
    from event_participants
    where validity = 'Rejected' and event_id = {event_id};
    """.format(event_id=event_id))
#View all past/upcoming events
def view_all_events(club_id, timeline):
    if timeline == 'Past':
        return dbf.query_db("""
        select * 
        from events
        # where club_id = {club_id} and datetime(date || ' ' || time) < CURRENT_TIMESTAMP
        order by date, time DESC;""".format(club_id=club_id))
    else:
        return dbf.query_db("""
        select *
        from events
        where club_id = {club_id} and datetime(date || ' ' || time) >= CURRENT_TIMESTAMP
        order by date, time;
        """.format(club_id=club_id))
                        
                                    
#-----------editing events---------------------
#retrieving event details to be displayed in the form
def get_event_details(event_id):
    event_details = dbf.query_db("""
    select *
    from events
    where event_id = {event_id};
    """.format(event_id=event_id))[0]
    return event_details

def add_event(club_id, event_name, event_description, event_date, event_time, event_location):
    dbf.modify_db("""
    insert into events(club_id, event_name, event_description, date, time, venue)
    values({club_id}, '{event_name}', '{event_description}', '{date}', '{time}', '{event_location}');
    """.format(club_id=club_id, event_name=event_name, event_description=event_description, date=event_date, time=event_time, event_location = event_location))

def update_event(event_id, event_name, event_description, event_date, event_time ,event_location):
    dbf.modify_db("""
    update events
    set event_name = '{event_name}', event_description = '{event_description}', venue = '{event_location}', date = '{date}', time = '{time}', updated = CURRENT_TIMESTAMP
    where event_id = {event_id};
    """.format(event_id=event_id, event_name=event_name, event_description=event_description, date=event_date, time=event_time, event_location = event_location))




################################################
def get_club_id(coordinator_id):
    return dbf.query_db("""
    select club_id
    from clubs
    where creator = {coordinator_id};
    """.format(coordinator_id=coordinator_id))[0][0]