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

    return render_template("index.html")


@app.route("/data/<team>", methods=["GET", "POST"])
def data(team):
    db = Database()
    data, col_name_trans = db.sprjoint_table_view()

    if request.method == "POST":
        formdata = request.form.to_dict()
        del formdata["button"]
        db.table_insert(table="sprjoint", row=formdata)

        return redirect(url_for("data", team=team))

    return render_template("data.html", data=data, col_name_trans=col_name_trans, team=team)


if __name__ == "__main__":
    app.run(debug=True)
