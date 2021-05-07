import dash
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

from datatable import create_datatable
from db import Database

app = Flask(__name__)
app.config["SECRET_KEY"] = "doe-corrosion-joint"

# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = "login"

# Dashapp
dashapp = dash.Dash(
    __name__,
    server=app,
    url_base_pathname="/dashapp/",
    assets_folder="static/dashassets",
    external_scripts=[
        "https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML",
    ],
)

dashapp.layout = create_datatable(data=[{"init": "test"}])


@app.route("/dashapp")
def dash_app():
    return dashapp.index()


@app.route("/", methods=["GET"])
def index():

    return render_template("index.html")


@app.route("/search/<table>", methods=["GET", "POST"])
def search(table):
    db = Database()

    # Table
    data, col_name_trans = db.table_view(table=table)

    dashapp.layout = create_datatable(data, col_name_trans)

    if request.method == "POST":
        formdata = request.form.to_dict()

        if formdata["button"] == "insert":
            del formdata["button"]
            db.table_insert(table=table, row=formdata)

        elif formdata["button"] == "delete":
            del formdata["button"]
            db.table_delete(table=table, row=formdata)

        elif formdata["button"] == "update":
            del formdata["button"]
            db.table_update(table=table, row=formdata)

        return redirect(url_for("search", table=table))

    return render_template("search.html", col_name_trans=col_name_trans, table=table)


@app.route("/phase")
def phase():
    return render_template("phase.html")


# Error Page
@app.errorhandler(500)
def internal_error(error):
    return render_template("error_pages/500.html"), 500


if __name__ == "__main__":
    app.run(debug=True)
