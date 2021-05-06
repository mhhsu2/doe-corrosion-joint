import os

import pymysql
import yaml


class Database:
    def __init__(self) -> None:
        CREDENTIAL_DIR = ".credentials"
        db_credential = yaml.load(
            open(os.path.join(CREDENTIAL_DIR, "db.yaml")), Loader=yaml.FullLoader
        )
        host = db_credential["mysql_host"]
        user = db_credential["mysql_user"]
        password = db_credential["mysql_password"]
        db = db_credential["mysql_db"]

        self.con = pymysql.connect(
            host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor
        )
        self.cur = self.con.cursor()

    def get_table(self, table: str):
        query = f"""
        SELECT *
        FROM {table}
        LIMIT 1000
        """

        self.cur.execute(query)
        result = self.cur.fetchall()
        return result

    def table_insert(self, table, row):
        keys = ", ".join(f"{k}" for k, v in row.items() if v is not "")
        values = ", ".join(f"'{v}'" for v in row.values() if v is not "")

        query = f"""
        INSERT INTO {table} ({keys})
        VALUES ({values})
        """

        self.cur.execute(query)
        self.con.commit()

    def table_delete(self, table, row):
        id = [*row.values()][0]

        query = f"""
        DELETE FROM {table}
        WHERE id_{table} = {id}
        """

        self.cur.execute(query)
        self.con.commit()

    def table_update(self, table, row):
        id = [*row.values()][0]
        pairs = ", ".join(f"{k} = '{v}'" for k, v in row.items() if v is not "")

        query = f"""
        UPDATE {table}
        SET {pairs}
        WHERE id_{table} = {id}
        """

        self.cur.execute(query)
        self.con.commit()

    def umich_table_view(self):
        query = f"""
        SELECT *
        FROM umich
        """

        self.cur.execute(query)
        result = self.cur.fetchall()

        db_col_names = result[1].keys()
        display_col_names = [
            "Id",
            "Joint Type",
            "Velocity (mm/s)",
            "Al Thickness (mm)",
            "Steel Thickness (mm)",
            "Rivet Diameter (mm)",
            "Rivet Length (mm)",
            "Corrosion Hours (h)",
            "Al 1 Material Loss Ratio",
            "Al 2 Material Loss Ratio",
            "Zone I Material Loss Ratio",
            "Zone II Material Loss Ratio",
            "Zone III Material Loss Ratio",
            "Zone IV Material Loss Ratio",
            "Zone V Material Loss Ratio",
            "Steel 1 Material Loss Ratio",
            "Zone 1 Width (mm)",
            "Min Stiffness (kN/mm)",
            "Max Stiffness (kN/mm)",
            "Avg Stiffness (kN/mm)",
            "Min Failure Load (kN)",
            "Max Failure Load (kN)",
            "Avg Failure Load (kN)",
            "Min Absorbed Energy (J)",
            "Max Absorbed Energy (J)",
            "Avg Absorbed Energy (J)",
        ]
        if len(db_col_names) == len(display_col_names):
            col_names_trans = dict(zip(db_col_names, display_col_names))
        else:
            print("Errors. Check columns from database and specificed columns.")
        return result, col_names_trans

    def psu_product_rsw_table_view(self):
        query = f"""
        SELECT *
        FROM psu_corrosion_product_rsw
        """

        self.cur.execute(query)
        result = self.cur.fetchall()

        db_col_names = result[1].keys()
        display_col_names = [
            "Id",
            "Cycles",
            "Al Coupled",
            "Al Uncoupled",
            "Fe Coupled",
            "Fe Coupled",
        ]
        if len(db_col_names) == len(display_col_names):
            col_names_trans = dict(zip(db_col_names, display_col_names))
        else:
            print("Errors. Check columns from database and specificed columns.")
        return result, col_names_trans


if __name__ == "__main__":
    # Test db connection
    db = Database()
    print(f"Connected: {db.con.open}")

    # Test table
    result = db.get_table(table="umich")
    print(result)
    import pdb

    pdb.set_trace()
