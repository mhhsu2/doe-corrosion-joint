from flask import Flask, redirect, render_template, request, session, url_for
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_manager,
    login_required,
    login_user,
    logout_user,
)

from db import Database

app = Flask(__name__)
app.config["SECRET_KEY"] = "doe-corrosion-joint"

# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = "login"


@app.route("/", methods=["GET"])
def index():

    return render_template("exp_info.html")


if __name__ == "__main__":
    app.run(debug=True)