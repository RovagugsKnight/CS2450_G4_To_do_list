import sqlite3

class Database:
    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def execute(self, query, *args):
        result = self.cursor.execute(query, args)
        self.connection.commit()
        return result

    def close(self):
        self.connection.close()