import dash
import dash_table

from db import Database

db = Database()
data, col_name_trans = db.sprjoint_table_view()
# print(data)

app = dash.Dash(__name__, assets_folder="static/dashassets")

app.layout = dash_table.DataTable(
    id="table",
    columns=[{"name": dis, "id": db} for db, dis in col_name_trans.items()],
    data=data,
    style_data_conditional=[{"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)"}],
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
    export_format="xlsx",
    export_headers="display",
)

if __name__ == "__main__":
    app.run_server(debug=True)
