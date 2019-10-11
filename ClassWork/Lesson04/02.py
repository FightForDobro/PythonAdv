import re
import time


class Client:
    """
    Class describe one client connection
    """

    DATABASE = {'fight': {'login': 'fight', 'name': 'Denys', 'surname': 'Ushakov', 'password': 'Qwerty1488!', 'reg_data': '10/11/19', 'user_post': [], 'is_admin': True}}
    ALLPOSTS = []

    @classmethod
    def validate(cls, user_data: dict):
        """
        Function validate all user input
        :param user_data: User data
        :return: False or user data
        """

        for key, value in user_data.items():

            if key == 'login' and value in Client.DATABASE.keys():
                print('User already exist')

                user_data[key] = input(f'Try better {key} ')
                return Client.validate(user_data)

            elif key == 'surname' and not value.isalpha():
                print('Invalid surname')

                user_data[key] = input(f'Try better {key} ')
                return Client.validate(user_data)

            elif key == 'name' and not value.isalpha():
                print('Invalid name')

                user_data[key] = input(f'Try better {key} ')
                return Client.validate(user_data)

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
                return Client.validate(user_data)

    class Registration:
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
            Client.DATABASE[self._login] = {key.replace('_', ''): value for (key, value) in self.__dict__.items()}
            Client.DATABASE[self._login].update({'reg_data': time.strftime('%D')})
            Client.DATABASE[self._login].update({'user_post': []})
            Client.DATABASE[self._login].update({'is_admin': False})
            print(Client.DATABASE)

        def __registration_status(self):
            """
            Function tells registration status
            """
            self.__database_update()

            if self._login in Client.DATABASE:
                print(f'{self._name.capitalize()} registration successful!')
                Client.Auth(self._login, self._password)

            else:
                print(f'{self._name.capitalize()} registration uncompleted!')

    class Auth:
        """
        Class describe registration status
        """

        def __init__(self, login: str, password: str):
            """
            Function construct data for Auth
            :param login: User login
            :param password: User password
            """
            self._login = login
            self._password = password

            self.user_validate()

        def user_validate(self):
            """
            Function validate user for auth
            """

            if self._login in Client.DATABASE:

                if self._password == Client.DATABASE[self._login]['password']:
                    print(f'Welcome {self._login}')
                    Client.Admin(self._login)

                else:
                    print('Password invalid')
                    Client.Auth(self._login, input('Password '))

            else:
                print('Login incorrect')
                Client.Auth(input('Login '), input('Password '))

    class User:
        """
        Class describe User
        """

        def __init__(self, login):
            """
            Function construct user
            :param login: User login
            """
            self._user_data = Client.DATABASE[login]

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

            if self._user_data.get('login') in Client.Admin(self._user_data['login']).is_admin():
                print('Enter A for go to Admin Menu')
            self.user_interface_logic()

        def user_interface_logic(self):
            """
            Function describe user interface logic
            """
            choice = input('Make your choice ')

            current_user = Client.Blog(self._user_data.get('login'), self._user_data.get('user_post', 0))

            if choice == '1':
                current_user.add_post()

            elif choice == '2':
                current_user.print_all_post()

            elif choice == '3':
                self.print_user_info()
                self.user_interface()

            elif choice == '4':
                Client.Interface().welcome()

            elif choice == 'A' and Client.Admin(self._user_data.get('login')).is_admin():
                Client.Admin(self._user_data.get('login'))

            else:
                Client.User(self._user_data['login'])

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

        @staticmethod
        def make_admin(login):
            """
            Function makes user admin
            :param login: User login
            """
            Client.DATABASE[login]['is_admin'] = True

        def is_admin(self):
            """
            Function check user have admin permission or not
            """

            if Client.DATABASE[self._user_data.get('login')]['is_admin']:
                self.mode_chooser()
            else:
                Client.User(self._user_data.get('login')).user_interface()

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
                Client.User(self._user_data['login']).user_interface()

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
            for number, user in enumerate(Client.DATABASE.keys()):
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

                    Client.User(temp_user_list[int(user_choice) - 1]).print_user_info()
                    self.user_control()

                elif choice == '2':
                    self.make_admin(temp_user_list[int(user_choice) - 1])
                    self.user_control()

                else:
                    self.mode_chooser()

    class Blog:
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
            self._all_post = Client.ALLPOSTS
            self._user_post = user_post

        def add_post(self):
            """
            Function adds post to blog
            """

            post_text = f'{input("Enter your text ")}\n' \
                        f'Post by: {self._current_user}\tDate: {time.strftime("%D")}'

            if post_text:
                self._all_post.append(post_text)
                Client.DATABASE[self._current_user]['user_post'].append(post_text)
                print('Post complete')
                Client.User(self._current_user).user_interface()

            else:
                print('Post uncompleted')
                Client.User(self._current_user).user_interface()

        def print_all_post(self):
            """
            Function prints all post from blog
            """

            for post in reversed(Client.ALLPOSTS):

                print('-----------------------------------')
                print(post, end='')
                print('\n-----------------------------------\n')

            input('Enter something to continue')
            Client.User(self._current_user).user_interface()

    class Interface:
        """
        Class describe interface
        """

        def welcome(self):
            """
            Prints welcome massage
            :return:
            """
            print('Welcome to Encrypt Social Network')
            self.new_user_logic()

        def new_user_logic(self):
            """
            Function describe user option
            :return: choice
            """
            print('Howdy! Human, the console of this world is open for you')

            choice = int(input('1. New Human\n'
                               '2. Old Human\n'))
            return self.sender(choice)

        @staticmethod
        def sender(choice):
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

                if Client.validate(reg_data):
                    return Client().Registration(*reg_data.values())

            elif choice == 2:
                return Client().Auth(input('Enter your login: ').lower(), input('Enter your password: '))


def start():
    """
    Function start single connection logic
    """
    return Client().Interface().welcome()


start()
