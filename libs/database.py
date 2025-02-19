from mysql.connector import connect, cursor
from libs.static_files_loader import load_config_file
from threading import Lock


def sql_str(string):
    return "'{}'".format(string)


class database:
    lock = Lock()
    insert_query = "INSERT INTO {} VALUES {};"
    delete_query = "DELETE FROM {} WHERE {};"
    edit_query = "UPDATE {} SET {} WHERE {};"
    select_query = "SELECT FROM {} WHERE {}"

    def __init__(self):
        config = load_config_file()["database"]
        self.connection = connect(
            host=config["host"],
            port=config["port"],
            username=config["username"],
            password=config["password"],
            database=config["database"],
            charset="utf8mb4",
            collation="utf8mb4_general_ci",
        )
        self.cursor = self.connection.cursor()

    # execute a query and return result if there in any
    def query(self, sql_query):
        with self.lock:
            self.cursor.execute(sql_query)
            return self.cursor.fetchall()

    # insert a new record
    def insert_row(self, table, data):
        sql_query = self.insert_query.format(table, data)
        with self.lock:
            self.cursor.execute(sql_query)
        return self.cursor.fetchall()

    # delete a record
    def delete_row(self, table, data, condition):
        pass

    # edit a record
    def edit_row(self, table, data, condition):
        sql_query = self.edit_query.format(table, data, condition)
        with self.lock:
            self.cursor.execute(sql_query)
        return self.cursor.fetchall()

    # get a record
    def get_row(self, table, condition):
        sql_query = self.select_query.format(table, condition)
        with self.lock:
            self.cursor.execute(sql_query)
        return self.cursor.fetchall()
