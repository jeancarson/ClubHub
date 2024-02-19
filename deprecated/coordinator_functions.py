# from sqlite3 import Cursor
# from sqlite3.dbapi2 import _CursorT
# from tkinter import _Cursor
#
# import db_functions as dbf
#
# import edit_club_details as ecd
#
#
# def save_club_details(club_id, club_name, club_description):
#     dbf.query_db(ecd.save_club_details.format(club_id=club_id, club_name=club_name,
#     club_description=club_description))
#
#
# def view_pending_members(club_id):
#     Cursor.execute(ecd.view_pending_members.format(club_id=club_id))
#     return cursor.fetchall()
#
#
# def view_approved_members(club_id):
#     cursor.execute(ecd.view_approved_members.format(club_id=club_id))
#     return cursor.fetchall()
#
#
# def view_pending_participants(event_id):
#     cursor.execute(ecd.view_pending_participants.format(event_id=event_id))
#     return _Cursor.fetchall()
#
#
# def view_approved_participants(event_id):
#     cursor.execute(ecd.view_approved_participants.format(event_id=event_id))
#     return _CursorT.fetchall()
#
#
# def save_members(club_id, user_id, new_validity):
#     cursor.execute(ecd.save_members.format(club_id=club_id, user_id=user_id, new_validity=new_validity))
#
#
# def save_participants(event_id, user_id, new_validity):
#     cursor.execute(ecd.save_participants.format(event_id=event_id, user_id=user_id, new_validity=new_validity))
#
#
# def delete_members(club_id):
#     cursor.execute(ecd.delete_members.format(club_id=club_id))
#
#
# def delete_participants(event_id):
#     cursor.execute(ecd.delete_participants.format(event_id=event_id))
#
#
# def add_member(club_id, user_id):
#     cursor.execute(ecd.add_member.format(club_id=club_id, user_id=user_id))
#
#
# def add_participant_member(event_id, user_id):
#     cursor.execute(ecd.add_participant_member.format(event_id=event_id, user_id=user_id))
#
#
# def add_participant_non_member(event_id, user_id):
#     cursor.execute(ecd.add_participant_non_member.format(event_id=event_id, user_id=user_id))
#
#
# def insert_new_event(club_id, event_name, event_description, timestamp):
#     cursor.execute(
#         ecd.insert_new_event.format(club_id=club_id, event_name=event_name, event_description=event_description,
#                                     timestamp=timestamp))
#
#
# def view_upcoming_events(club_id):
#     cursor.execute(ecd.view_all_upcoming_events.format(club_id=club_id))
#     return cursor.fetchall()
#
#
# def view_past_events(club_id):
#     cursor.execute(ecd.view_past_events.format(club_id=club_id))
#     return cursor.fetchall()
#
#
# def view_single_event(event_id):
#     cursor.execute(ecd.view_single_event.format(event_id=event_id))
#     return cursor.fetchone()
#
#
# def num_approved_members():
#     cursor.execute(ecd.count_approved_members)
#     result = cursor.fetchone()
#     return result[0] if result else 0
#
#
# def num_pending_members():
#     cursor.execute(ecd.count_pending_members)
#     result = cursor.fetchone()
#     return result[0] if result else 0
#
#
# def num_approved_participants():
#     cursor.execute(ecd.count_approved_participants)
#     result = cursor.fetchone()
#     return result[0] if result else 0
#
#
# def num_pending_participants():
#     cursor.execute(ecd.count_pending_participants)
#     result = cursor.fetchone()
#     return result[0] if result else 0
#
#
# def get_limited_view_events(club_id):
#     cursor.execute(ecd.limited_view_all_upcoming_events.format(club_id=club_id))
#
#
# def test():
#     print("Hello")
