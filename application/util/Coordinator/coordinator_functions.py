import edit_club_details as ecd
import __init__ as init

def save_club_details(club_id, club_name, club_description):
    cursor.execute(ecd.save_club_details.format(club_id=club_id, club_name=club_name, club_description=club_description))