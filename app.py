import dash
import dash_table
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
    dashapp.layout = dash_table.DataTable(
        id="table",
        columns=[{"name": dis, "id": db} for db, dis in col_name_trans.items()],
        data=data,
        style_data_conditional=[
            {"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)"}
        ],
        style_header={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold"},
        style_cell={
            # all three widths are needed
            "minWidth": "240px",
            "width": "240px",
            "maxWidth": "240px",
        },
        editable=True,
        sort_action="native",
        filter_action="native",
        page_action="native",
        page_size=25,
        export_format="xlsx",
        export_headers="display",
    )

    if request.method == "POST":
        formdata = request.form.to_dict()

        if formdata["button"] == "insert":
            del formdata["button"]
            db.table_insert(table="sprjoint", row=formdata)

        elif formdata["button"] == "delete":
            del formdata["button"]
            db.table_delete(table="sprjoint", row=formdata)

        elif formdata["button"] == "update":
            del formdata["button"]
            db.table_update(table="sprjoint", row=formdata)

        return redirect(url_for("data", team=team))

    return render_template("data.html", data=data, col_name_trans=col_name_trans, team=team)


# Dashapp
db = Database()
d, col_name_trans = db.sprjoint_table_view()
dashapp = dash.Dash(
    __name__, server=app, url_base_pathname="/dashapp/", assets_folder="static/dashassets"
)

dashapp.layout = dash_table.DataTable(
    id="table",
    columns=[{"name": dis, "id": db} for db, dis in col_name_trans.items()],
    data=d,
    style_data_conditional=[{"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)"}],
    style_header={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold"},
    style_cell={
        # all three widths are needed
        "minWidth": "240px",
        "width": "240px",
        "maxWidth": "240px",
    },
    style_table={"overflowX": "auto"},
    editable=True,
    sort_action="native",
    filter_action="native",
    page_action="native",
    page_size=25,
    export_format="xlsx",
    export_headers="display",
)


@app.route("/dashapp")
def dash_app():
    return dashapp.index()


if __name__ == "__main__":
    app.run(debug=True)
