# Third party libraries
from flask import (
    Flask,
    render_template,
    session,
)

# Local modules
from modules.blueprints.login_logout import login_logout
from modules.blueprints.registration import registration


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


@app.route("/about")
@app.route("/about-us")
def about_us() -> str:
    """
    Loads the about page.
    """

    return render_template("about.html")


if __name__ == '__main__':
    app.run()
