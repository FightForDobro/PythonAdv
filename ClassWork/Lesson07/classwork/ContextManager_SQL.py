import sqlite3


class ContextManagerSql:

    def __init__(self, name):
        self._name = name

    def __enter__(self):

        self.conn = sqlite3.connect(self._name)
        return self.conn.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()


with ContextManagerSql('/Users/FightForDObro/Desktop/Курсы/PythonAdv/PythonAdv/ClassWork/Lesson07/lesson07.db') as db:
    sql = '''SELECT * FROM user'''
    query_response = db.execute(sql)

    print(query_response.fetchall())
