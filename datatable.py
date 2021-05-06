import dash
import dash_table

from db import Database


def create_datatable(data: dict, col_name_trans: dict = None) -> dash_table.DataTable:
    if col_name_trans is not None:
        columns = [{"name": dis, "id": db} for db, dis in col_name_trans.items()]
    else:
        columns = [{"name": k, "id": k} for k in data[0].keys()]

    return dash_table.DataTable(
        id="table",
        columns=columns,
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
        sort_action="native",
        filter_action="native",
        # page_action="native",
        # page_size=25,
        export_format="xlsx",
        export_headers="display",
    )


if __name__ == "__main__":
    db = Database()
    data, col_name_trans = db.table_view(table="psu_corrosion_product_spr")

    app = dash.Dash(
        __name__,
        assets_folder="static/dashassets",
        external_scripts=[
            "https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML",
        ],
    )

    ## Test datatable
    app.layout = create_datatable(data, col_name_trans)

    app.run_server(debug=True)
