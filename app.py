# Third party libraries
from flask import (
    Flask,
    render_template,
    session,
)

# Local modules
from modules.blueprints.login import login


app: Flask = Flask(__name__)
app.register_blueprint(login)

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


if __name__ == '__main__':
    app.run()
