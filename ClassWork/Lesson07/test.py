# import sqlite3
#
# conn = sqlite3.connect('student.db')
# conn.cursor()
#
# conn.execute(f'''update students_table set {'user_role'}=? where student_id=?''', ('user', '1'))
#
# conn.commit()
# conn.close()


def f():
    print('Hello World!')


d_c = {'a': f()}

d_c['a']
