import sqlite3


class DB:

    def __init__(self):
        self._db_name = 'student.db'

    def get_auth_data(self):

        conn = sqlite3.connect(self._db_name)
        conn.cursor()

        users = conn.execute('''select * from students_table''')
        users_data = users.fetchall()
        names = []
        conn.close()

        return users_data

    def receive_command(self, command, *args):

        conn = sqlite3.connect(self._db_name)
        conn.cursor()
        try:
            received_information = conn.execute(command, args)
        except ValueError:
            received_information = conn.execute(command[0], str(command[1]))

        try:

            data = received_information.fetchall()
            names = [name[0] for name in received_information.description]
            conn.commit()
            conn.close()

        except TypeError:
            return

        return data, names


class Interface:

    def __init__(self, cur_user=None):

        self._cur_user = cur_user
        self._cur_user_role = None

    def print_interface(self):

        self._cur_user_role = self.get_role()[0]

        for key in self.sql_command_list():

            if key.startswith(('6', '7', '8', '9')) and self._cur_user_role != 'admin':
                continue
            print(f'{key}\n')

        choice = input('Choose ')

        if 0 <= int(choice) < 9:
            self.sql_sender(choice)
        else:
            return self.print_interface()

    def welcome(self):
        print('Welcome to MIT\'s Student Network\n')
        usr_inp = input('Press something to login or 0 to exit\n')

        if usr_inp == '0':
            exit('Bye!')

        Auth().auth_logic()

    def sql_command_list(self):

        commands = {
            '1.Get all users': '''select * from students_table''',
            '2.Get all marks': '''select * from marks_table''',
            '3.Get own information': ('''select * from students_table where id = ?''', self._cur_user),
            '4.Get list of excellence': '''select * from marks_table where average_mark > 80''',
            '5.Get info about student': '''select * from students_table inner join marks_table mt on students_table.student_id = mt.student_id where students_table.student_id = ?''',
            '6.ADMIN ADD STUDENT': '''insert into students_table(name, surname, faculty, course, student_id, user_role) values (?, ?, ?, ?, ?, ?)''',
            '7.ADMIN. EDIT STUDENT': '''update students_table set ?=? where student_id=?''',
            '8.ADMIN MAKE ADMIN': '''update students_table set user_role='admin' where student_id=?''',
            '9.ADMIN DELETE STUDENT': '''delete from students_table where student_id = ?''',
            '0. Exit': 0
        }

        return commands

    def get_role(self):

        role = DB().receive_command('''select user_role from students_table where student_id = ?''', self._cur_user)
        return role[0][0]

    def sql_sender(self, choice):

        arguments = []
        if choice == '0':
            return Interface().welcome()

        elif choice == '6':

            arguments.append(input('Enter student name: \n'))
            arguments.append(input('Enter student surname: \n'))
            arguments.append(input('Enter student faculty: \n'))
            arguments.append(input('Enter student course: \n'))
            arguments.append(input('Enter student id: \n'))
            arguments.append(input('Enter student role: \n'))

        elif choice == '7':

            arguments.append(input('Enter column title: \n'))
            arguments.append(input('Enter new info: \n'))
            arguments.append(input('Enter student id: \n'))

        elif choice == '5' or choice == '8' or choice == '9':

            arguments.append(input('Enter student id: \n'))

        for key, value in self.sql_command_list().items():

            if key.startswith(choice):

                if arguments:
                    data = DB().receive_command(value, *arguments)
                    self.pretty_info(data)
                    input('Enter something to continue')
                    self.print_interface()

                else:
                    data = DB().receive_command(value)
                    self.pretty_info(data)
                    input('Enter something to continue')
                    self.print_interface()

        raise KeyError('No such command')

    def pretty_info(self, data):
        for user in data[0]:

            pretty_info = {key: value for key, value in zip(data[1], user)}
            print('------------------------------')
            for name, info in pretty_info.items():
                print(f'{name}: {info}')

class Auth:

    def auth_logic(self):

        student_id = int(input('Student id:\n'))
        # name = input('Name: \n')
        # surname = input('Surname: \n')

        if self.validator(student_id):
            User(student_id).user_logic()
        else:
            return self.auth_logic()

    def validator(self, usr_inp):

        for user in DB().get_auth_data():
            if usr_inp in user[1:]:
                return user

        return False


class User:

    def __init__(self, current_user):
        self._current_user = current_user

    def user_logic(self):
        Interface(self._current_user).print_interface()


class Admin(User):

    def __init__(self, current_user):
        super().__init__(current_user)

    def admin_logic(self):
        Interface(self._current_user).print_interface()


Interface().welcome()
