from PyQt6.QtSql import *


class DatabaseManager:

    def __init__(self, db_name):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(db_name)
        self.con = self.db.open()
        if not self.con:
            exit("Can't connect to DB")

    def execute_query(self, query_str, values=None):
        query = QSqlQuery(self.db)
        query.prepare(query_str)
        if values:
            for element in values:
                query.addBindValue(element)
        query.exec()
        return query