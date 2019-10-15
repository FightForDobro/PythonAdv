import re
import time
import shelve


class Client:
    """
    Class describe all client Data
    """
    def open_db(self, db_branch):
        """
        Function opens database
        :param db_branch: DataBase branch User or All post
        :return: DataBase
        """

        with shelve.open('main_db') as db:
            if len(db) == 0:
                db['Users'] = {}
                db['All_Posts'] = []

        with shelve.open('main_db') as db:
            return db[db_branch]

    def write_db(self, db_branch: str, *args):
        """
        Function writes data to the database
        :param db_branch: DataBase branch User or All post
        :param args: some data
        :return:
        """

        with shelve.open('main_db', writeback=True) as db:

            if db_branch == 'Users':

                if 'is_admin' in args:
                    db[db_branch][args[0]][args[1]] = args[2]

                elif type(args[1]) is not dict and 'is_admin' not in args:
                    db[db_branch][args[0]]['user_post'].append(args[1])

                else:
                    db[db_branch][args[0]] = args[1]

            elif db_branch == 'All_Posts':
                db[db_branch].append(args[0])

            else:
                print('Invalid branch')


class Validators(Client):
    """
    Class describe validators
    """

    def user_input_validator(self, user_data: dict):
        """
        Function validate all user input
        :param user_data: User data
        :return: False or user data
        """

        for key, value in user_data.items():

            if key == 'login' and value in self.open_db('Users'):
                print('User already exist')

                user_data[key] = input(f'Try better {key} ')
                return self.user_input_validator(user_data)

            elif key == 'surname' and not value.isalpha():
                print('Invalid surname')

                user_data[key] = input(f'Try better {key} ')
                return self.user_input_validator(user_data)

            elif key == 'name' and not value.isalpha():
                print('Invalid name')

                user_data[key] = input(f'Try better {key} ')
                return self.user_input_validator(user_data)

            elif key == 'password':

                while True:

                    if len(value) < 8:
                        print('Password has to be longer then 8 symbols')
                        break

                    elif not re.search('[a-z]', value):
                        print('Password should contain lower letter')
                        break

                    elif not re.search('[A-Z]', value):
                        print('Password should contain upper letter')
                        break

                    elif not re.search('[0-9]', value):
                        print('Password should contain numbers')
                        break

                    elif not re.search('[\W]', value):
                        print('Password should contain punctuation')
                        break

                    elif re.search('[\s]', value):
                        print('Password shouldn\'t contain spaces')

                    else:
                        return True

                user_data[key] = input(f'Try better {key} ')
                return self.user_input_validator(user_data)

    def user_validate(self, login, password):
        """
        Function user_input_validator user for auth
        """

        if login in self.open_db('Users'):

            if password == self.open_db('Users')[login]['password']:
                print(f'Welcome {login}!')
                Admin(login)

            else:
                print('Password invalid')
                self.user_validate(login, input('Password '))

        else:
            print('Login incorrect')
            self.user_validate(input('Login '), input('Password '))


class Auth(Validators):
    """
    Class describe Auth
    """

    def __init__(self, login: str, password: str):
        """
        Function construct data for Auth
        :param login: User login
        :param password: User password
        """

        self.user_validate(login, password)


class Registration(Client):
    """
    Class describe registration
    """

    def __init__(self, login: str, surname: str, name: str, password: str):
        """
        Function construct new user
        :param login: User ID
        :param surname: User surname
        :param name: User name
        :param password: User Password
        """
        self._login = login
        self._name = name
        self._surname = surname
        self._password = password

        self.__registration_status()

    def __database_update(self):
        """
        Add user to data base
        """
        user_data = {key.replace('_', ''): value for (key, value) in self.__dict__.items()}
        user_data.update({'reg_data': time.strftime('%D')})
        user_data.update({'user_post': []})
        user_data.update({'is_admin': False})
        return self.write_db('Users', self._login, user_data)

    def __registration_status(self):
        """
        Function tells registration status
        """
        self.__database_update()

        if self._login in self.open_db('Users'):
            print(f'{self._name.capitalize()} registration successful!')
            Auth(self._login, self._password)

        else:
            print(f'{self._name.capitalize()} registration uncompleted!')


class Blog(Client):
    """
    Class describe blog
    """

    def __init__(self, user, user_post):
        """
        Function construct data for blog
        :param user: User login
        :param user_post: User posts
        """
        self._current_user = user
        self._all_post = self.open_db('All_Posts')
        self._user_post = user_post

    def add_post(self):
        """
        Function adds post to blog
        """

        post_text = f'{input("Enter your text ")}\n' \
                    f'Post by: {self._current_user}\tDate: {time.strftime("%D")}'

        if post_text:
            self.write_db('All_Posts', post_text)
            self.write_db('Users', self._current_user, post_text)
            print('Post complete')
            User(self._current_user).user_interface()

        else:
            print('Post uncompleted')
            User(self._current_user).user_interface()

    def print_all_post(self):
        """
        Function prints all post from blog
        """

        for post in reversed(self.open_db('All_Posts')):
            print('-----------------------------------')
            print(post, end='')
            print('\n-----------------------------------\n')

        input('Enter something to continue')
        User(self._current_user).user_interface()


class User(Client):
    """
    Class describe User
    """

    def __init__(self, login):
        """
        Function construct user
        :param login: User login
        """
        self._user_data = self.open_db('Users')[login]

    def user_interface(self):
        """
        Function prints user interface
        """
        print(f'Current profile: {self._user_data.get("login").capitalize()} '
              f'Registration date: {self._user_data.get("reg_data")} '
              f'Post count: {len(self._user_data.get("user_post"))}')
        print('1. Make Post\n'
              '2. View all Posts\n'
              '3. View personal profile\n'
              '4. Exit\n')

        if self.open_db('Users')[self._user_data['login']]['is_admin']:
            print('Enter A for go to Admin Menu')

        self.user_interface_logic()

    def user_interface_logic(self):
        """
        Function describe user interface logic
        """
        choice = input('Make your choice ')

        current_user = Blog(self._user_data.get('login'), self._user_data.get('user_post', 0))

        if choice == '1':
            current_user.add_post()

        elif choice == '2':
            current_user.print_all_post()

        elif choice == '3':
            self.print_user_info()
            self.user_interface()

        elif choice == '4':
            Interface().welcome()

        elif choice == 'A' and self.open_db('Users')[self._user_data['login']]['is_admin']:
             Admin(self._user_data.get('login'))

        else:
            self.user_interface()

    def print_user_info(self):
        """
        Function prints user info
        """

        print('Personal info')
        for key, value in self._user_data.items():

            try:
                print(f'{key.capitalize()}: {value.capitalize()}')

            except AttributeError:
                print(f'{key.capitalize()}: {value}')

        input('\nEnter something to continue')


class Admin(User):
    """
    Class describe admin
    """

    def __init__(self, login):
        """
        Function construct
        :param login: Admin login
        """
        super().__init__(login)

        self.is_admin()

    def make_admin(self, login):
        """
        Function makes user admin
        :param login: User login
        """
        self.write_db('Users', login, 'is_admin', True)

    def is_admin(self):
        """
        Function check user have admin permission or not
        """

        if self.open_db('Users')[self._user_data.get('login')]['is_admin']:
            self.mode_chooser()
        else:
            User(self._user_data.get('login')).user_interface()

    def mode_chooser(self):
        """
        Function prints admin option
        :return:
        """
        print('1. ADMIN MENU')
        print('2. USER MENU')

        choice = input('Choose ')

        if choice == '1':
            self.admin_menu()

        elif choice == '2':
            User(self._user_data['login']).user_interface()

        else:
            self.mode_chooser()

    def admin_menu(self):
        """
        Function describe admin menu
        """
        print('1. All users')

        choice = input('Choose ')

        if choice == '1':
            self.user_control()

        else:
            self.admin_menu()

    def user_control(self):
        """
        Function give option of control on user
        """

        temp_user_list = []
        for number, user in enumerate(self.open_db('Users').keys()):
            print(f'{number + 1}: {user}')
            temp_user_list.append(user)

        user_choice = input('Choose user or press enter to get back')

        if not user_choice:
            self.mode_chooser()

        else:
            print('1. View profile')
            print('2. Make ADMIN')
            choice = input('Make your choice ')

            if choice == '1':

                User(temp_user_list[int(user_choice) - 1]).print_user_info()
                self.user_control()

            elif choice == '2':
                self.make_admin(temp_user_list[int(user_choice) - 1])
                self.user_control()

            else:
                self.mode_chooser()


class Interface(Validators):

    def welcome(self):
        """
        Prints welcome message and start user logic function
        """
        print('Welcome to Encrypt Social Network')
        time.sleep(0.5)
        print('Howdy! Human, the console of this world is open for you')
        self.new_user_logic()

    def new_user_logic(self):
        """
        Function describe user option
        :return: choice
        """

        choice = int(input('1. New Human\n'
                           '2. Old Human\n'))
        if not 0 < choice < 3:
            print('Try again!')
            return self.new_user_logic()

        return self.sender(choice)

    def sender(self, choice):
        """
        Function send user choice to program logic register
        :param choice: Register or auth
        :return: Auth class or Register class
        """

        if choice == 1:

            reg_data = {
                'login': input('Enter your login: ').lower(),
                'surname': input('Enter your surname: '),
                'name': input('Enter your name: '),
                'password': input('Enter your password: ')
            }

            if self.user_input_validator(reg_data):
                return Registration(*reg_data.values())

        elif choice == 2:
            return Auth(input('Enter your login: ').lower(), input('Enter your password: '))


Interface().welcome()


