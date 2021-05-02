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


if __name__ == "__main__":
    # Test db connection
    db = Database()
    print(f"Connected: {db.con.open}")

    # Test table
    result = db.get_table(table="sprjoint")
    print(result)
    import pdb

    pdb.set_trace()
