from flask import Blueprint, jsonify, render_template, request

from application.util.db_functions.main import query_db
from application.util.db_functions.clubs import count_club_memberships, insert_club_membership

mia_blueprint = Blueprint("mia_blueprint", __name__)


@mia_blueprint.route("/user")
def user():
    """
    Loads the user MAIN page.
    """
    return render_template("html/student/student-main.html", header="User Page")


@mia_blueprint.route("/profile1")
def go_profile():
    return render_template("html/student/profile.html")  


@mia_blueprint.route("/clubs")
def go_clubs():
    return render_template("html/student/clubs.html")


# @mia_blueprint.route("/events")
def go_events():
    return render_template("html/student/events.html")


@mia_blueprint.route("/clubs", methods=["GET"])
def get_clubs():
    
    clubs_info = query_db("SELECT club_id, club_name, club_description FROM clubs")
    clubs = [(row['club_name'], row['club_description'], row['club_id']) for row in clubs_info]

    popular_clubs = clubs[:3]
    all_clubs = clubs
    return render_template("clubs.html", popular_clubs=popular_clubs, all_clubs=all_clubs)



@mia_blueprint.route("/signup", methods=["POST"])
def signup():
    user_id = request.form.get("userId")
    club_id = request.form.get("clubId")
    
    try:
        # I THINK THIS SHOULD WORK
        count = count_club_memberships(user_id)
        if count >= 3:
            return jsonify({"success": False, "message": "You are already a member of three clubs."}), 400
        
        
        insert_club_membership(club_id, user_id)
        
        return jsonify({"success": True, "message": "Signed up successfully"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
