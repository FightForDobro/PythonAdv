# TODO Добаить флажки к функции чтобы принтить
# TODO Исправить возможность инекции (Добавить валидатор чтобы данные входили нужные )
# TODO Поменять листси на реаляцыоную бауз
import sqlite3


class DBContextManager:

    def __init__(self, db_name='student.db'):
        self._db_name = db_name

    def __enter__(self):
        self.conn = sqlite3.connect(self._db_name)
        return self.conn.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()


class DB:

    def add_user(self):

        new_user_data = {'name': 'User name: ',
                         'surname': 'User surname: ',
                         'faculty': 'User faculty: ',
                         'course': 'User course: ',
                         'student_id': 'User student id: ',
                         'user_role': 'User user role: ',
                         }

        for key, value in new_user_data.items():

            while True:

                new_value = input(value).lower()

                if not value:
                    print(f'{key} field cannot be empty')
                    continue

                elif key == 'student_id' and any(str(id[0]) == new_value for id in self.get_all_students_id()):
                    print(f'{new_value} id is already in use')
                    continue

                elif key == 'user_role' and not any(role[0] == new_value for role in self.get_all_roles()):
                    print(f'{key}: {new_value} doesnt exist')
                    continue

                new_user_data[key] = new_value
                break

        with DBContextManager() as db:
            sql = '''insert into students_table(name, surname, faculty, course, student_id, user_role) 
            values (?, ?, ?, ?, ?, ?)'''
            db.execute(sql, tuple(new_user_data.values()))
            db.execute('''insert into marks_table(student_id) values (?)''', tuple(new_user_data.values())[4])

            return f'{list(new_user_data.values())[0]} added to DataBase'

    def edit_user(self):

        while True:

            edit_user = input('Enter student id: ')

            if any(str(id[0]) == edit_user for id in self.get_all_students_id()):
                break

            else:
                print(f'No such id {edit_user}')
                continue

        print('\t\t---Which field you want to change---')
        self.pretty_info(self.get_user_data(edit_user))

        possible_field = self.get_user_data(edit_user)[1]
        restricted_fields = ('id', 'student_id', 'user_role')
        while True:

            filed = input('Enter here --> ').lower()
            new_info = input('New info --> ').lower()

            if filed not in possible_field:
                print(f'{filed} no such field')
                continue

            elif filed in restricted_fields:
                print(f'You cant edit {filed} :(')
                continue
            break

        with DBContextManager() as db:
            sql = f'''update students_table set {filed}=? where student_id=?'''
            db.execute(sql, (new_info, edit_user))
            return f'Edit complete {filed} = {new_info} student: {edit_user}'

    def delete_user(self):

        while True:
            student_id = input('Enter student ID --> ')

            if any(str(id[0]) == student_id for id in self.get_all_students_id()):
                break

            else:
                print(f'No such id {student_id}')
                continue

        with DBContextManager() as db:
            sql = 'delete from students_table where student_id = ?'
            db.execute(sql, student_id)
            return f'Student {student_id} deleted'

    def get_all_students(self):

        with DBContextManager() as db:
            sql = 'select * from students_table inner join marks_table mt on students_table.student_id = mt.student_id'
            query_response = db.execute(sql)
            names = [name[0] for name in query_response.description]
            return query_response.fetchall(), names

    def get_all_students_id(self):

        with DBContextManager() as db:
            sql = 'select student_id from students_table'
            query_response = db.execute(sql)
            return query_response.fetchall()

    def get_list_of_excellent(self):

        with DBContextManager() as db:

            sql = '''select * from students_table 
            inner join marks_table mt on students_table.student_id = mt.student_id
            where average_mark >= 80'''
            query_response = db.execute(sql)
            names = [name[0] for name in query_response.description]

            return query_response.fetchall(), names

    def get_all_roles(self):

        with DBContextManager() as db:
            sql = 'select role_title from role'
            query_response = db.execute(sql)
            return query_response.fetchall()

    def get_user_data(self, user_id=None):

        if user_id is None:
            user_id = input('Enter student ID --> ')

        with DBContextManager() as db:

            sql = '''select * from students_table 
            left join marks_table mt on students_table.student_id = mt.student_id 
            where students_table.student_id=?'''
            query_response = db.execute(sql, user_id)
            names = [name[0] for name in query_response.description]
            return query_response.fetchall(), names

    def get_user_marks(self, student_id, lesson):

        with DBContextManager() as db:

            sql = f'''select {lesson} from marks_table where student_id=?'''
            query_response = db.execute(sql, student_id)
            return query_response.fetchall()


    def pretty_info(self, data):

        for user in data[0]:

            pretty_info = {key: value for key, value in zip(data[1], user)}
            for name, info in pretty_info.items():
                print(f'{name}: {info}')

        return pretty_info

    def cur_user_dict(self, usr_id):

        data = self.get_user_data(usr_id)

        for user in data[0]:

            cur_user_dict = {key: value for key, value in zip(data[1], user)}

            return cur_user_dict

    def add_marks(self, student_id, lesson, marks):

        with DBContextManager() as db:
            sql = f'update marks_table set {lesson}=? where student_id=?'
            db.execute(sql, (marks, student_id))
            return f'Student: {student_id} marks updated'


class Interface:

    def __init__(self, student_id=None):

        if student_id is not None:
            self._student_id = student_id
            self._cur_student = DB().cur_user_dict(student_id)

    def print_interface(self):

        for key in self.command_list():

            if key.startswith(('6', '7', '8', '9')) and self._cur_student['user_role'] != 'admin':
                continue
            print(f'{key}\n')

        choice = input('Choose ')

        if 0 < int(choice) < 8:
            self.sql_sender(choice)
        else:
            return self.print_interface()

    def command_list(self):

        commands = {
            '1.Get all users': DB().get_all_students,
            '2.Get own information': DB().get_user_data,
            '3.Get list of excellence': DB().get_list_of_excellent,
            '4.Get info about student': DB().get_user_data,
            '5.ADMIN ADD STUDENT': DB().add_user,
            '6.ADMIN. EDIT STUDENT': DB().edit_user,
            '7.ADMIN DELETE STUDENT': DB().delete_user,
            '8.ADMIN ADD MARKS': DB().add_marks,
            '0. Exit': 0
        }

        return commands

    def sql_sender(self, choice):

        if choice == '0':
            return Auth().login()

        for key, value in self.command_list().items():

            if key.startswith('2') and choice == '2':
                return DB().pretty_info(self.command_list()[key](self._student_id))

            elif key.startswith('8') and choice == '8':
                student_id = input('Enter Student ID -->')
                lesson = input('Enter Lesson --> ')
                marks = DB().get_user_marks(student_id, lesson)
                mark = input('Enter mark --> ')
                marks.append(int(mark))
                return DB().pretty_info(self.command_list()[key](student_id, lesson, marks))

            elif key.startswith(choice):
                return DB().pretty_info(self.command_list()[key]())

        raise KeyError('No such command')


class Auth:

    def login(self):

        print('---Welcome to StudentBase---')
        input('Press something to login ')

        student_id = input('Enter your student ID --> ')

        if any(str(id[0]) == student_id for id in DB().get_all_students_id()):
            Interface(student_id).print_interface()
        else:
            print('Try again!')
            self.login()


Auth().login()
# data = DB().get_list_of_excellent()
# DB().pretty_info(data)

# data = (DB().get_user_data('1'))
#
# DB().pretty_info(data)


# r = DB().get_all_students_id()
# print(r)
#
# print(any(str(id[0]) == '3' for id in r))

