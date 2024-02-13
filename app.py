# Third party libraries
from collections import UserString
from flask import (
    Flask,
    Response, 
    render_template,
    request,
    session,
    redirect,
)

# Local modules
from modules.blueprints.login_logout import login_logout
from modules.blueprints.registration import registration
from modules.general.user_auth import password_match


app: Flask = Flask(__name__)
app.register_blueprint(login_logout)
app.register_blueprint(registration)

# Load environment variables (from .env and .flaskenv)
app.config.from_prefixed_env()


@app.route("/") 
@app.route("/index")
@app.route("/home")
def home() -> str:
    """
    Loads the home (default) page.
    """

    if "user" in session:
        user: str = session["user"]
        return render_template("index.html", header=f"Hello {user}!")

    return render_template("index.html")

#admin redirect besties

@app.route("/members_info")
def members_info():
    return render_template('adminFolder/inform.html')

@app.route("/pending_users")
def pending_users():
    return render_template("adminFolder/pending.html")


@app.route("/admin")
def admin():
    
        return render_template("adminFolder/admin_main.html")


#users redirect 
@app.route("/user")
def user():
    """
    Loads the user MAIN page.
    """
    return render_template("usersFolder/user_main.html", header="User Page")

@app.route("/profile")
def go_profile():
    return render_template("usersFolder/profile.html")

@app.route("/clubss")
def go_clubs():
    return render_template("usersFolder/clubss.html")

@app.route("/eventss")
def go_events():
    return render_template("usersFolder/eventss.html")

@app.route("/about")
@app.route("/about-us")
def about_us():
    """
    Loads the about page.
    """
    return render_template("about.html")

@app.route("/login")
def login() -> str:
    """
    Loads the login page.
    """

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post() -> str | Response:
    """
    Function called when login button (from the login page) is pressed.
    """

    username: str = request.form["username"]
    password: str = request.form["password"]

    if "user" in session:
        current_user: str = session["user"]
        app.logger.warning(f"Login fail: {current_user!r} is already logged in")
        return render_template("login.html", error_message=f"You are already logged in as {current_user!r}")

    if not username:
        app.logger.warning("Login fail: Empty username")
        return render_template("login.html", error_message="Please enter a username")

    if username not in users:
        app.logger.warning(f"Login fail: User {username!r} does not exist")
        return render_template("login.html", error_message="User not found")

    hashed_pw: str = UserString[username]

    if not password_match(password, hashed_pw):
        app.logger.warning(f"Login fail: Incorrect password for user {username!r}")
        return render_template("login.html", error_message="Incorrect password")

    app.logger.info(f"Login success: {username!r}")

    # Create a user session
    session["user"] = username

    return redirect("/home")


if __name__ == '__main__':
    app.run()
