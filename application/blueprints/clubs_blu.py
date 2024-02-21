from flask import Blueprint, jsonify, redirect, render_template, request, session

from application.util.db_functions.main import query_db
from application.util.db_functions.clubs import count_club_memberships, get_popular_clubs, get_all_clubs, join_club

clubs_blu = Blueprint("clubs_blu", __name__)


@clubs_blu.route("/clubs_final")
def get_clubs():
    """
    Renders the clubs page.
    """
    popular_clubs = get_popular_clubs()
    all_clubs = get_all_clubs()
    return render_template("html/student/clubs.html", popular_clubs=popular_clubs, all_clubs=all_clubs)





@clubs_blu.route('/join', methods=['POST'])
def join_club_route():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        club_id = request.form.get('club_id')

        # Check if user_id or club_id is empty
        if not user_id or not club_id:
            return "User ID or Club ID is missing in the request."

        try:
            user_id = int(user_id)
            club_id = int(club_id)
        except ValueError:
            return "User ID or Club ID is not a valid integer."

        if count_club_memberships(user_id) >= 3:
            membership_limit = True
        else:
            membership_limit = False
            join_club(user_id, club_id)


        
    
    return redirect('/clubs_final', membership_limit=membership_limit) 
