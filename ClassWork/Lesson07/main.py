import sqlite3

conn = sqlite3.connect('lesson07.db')
cursor = conn.cursor()

login = input('Enter the login: ')
password = input('Enter pass: ')
sql = '''INSERT INTO user (login, password) VALUES(?, ?)'''  # СТАВИТЬ ПРОБЕЛИ

query_response = cursor.execute(sql, [login, password])
conn.commit()

conn.close()
