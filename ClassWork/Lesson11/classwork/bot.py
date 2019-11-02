import telebot
import ClassWork.Lesson11.config as config
from mongoengine import *

connect('telegram_db')


class UserData(DynamicDocument):
    user_id = IntField()
    name = StringField()
    surname = StringField()
    middle_name = StringField()
    phone = StringField()
    email = StringField()
    address = StringField()
    wishes = StringField()


bot = telebot.TeleBot(config.TOKEN)


know_users = []
user_step = {}


def get_user_step(uid):

    if uid in user_step:
        return user_step[uid]

    else:
        know_users.append(uid)
        user_step[uid] = 0
        return 0


@bot.message_handler(commands=['start'])
def start(message):

    cid = message.chat.id

    if cid not in know_users:

        know_users.append(cid)
        user_step[cid] = 0

        bot.send_message(message.chat.id, 'Hello im bot and i need your data :(+)')
        bot.send_message(message.chat.id, 'Enter your name:')
        UserData(user_id=message.from_user.id).save()

    else:
        bot.send_message(cid, 'Yoc cant add more data!')


@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 0)
def name(message):
    UserData.objects(user_id=message.from_user.id).update(name=message.text)
    bot.send_message(message.chat.id, 'Enter your surname:')
    user_step[message.from_user.id] = 1


@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)
def surname(message):
    UserData.objects(user_id=message.from_user.id).update(surname=message.text)
    bot.send_message(message.chat.id, 'Enter your middle name:')
    user_step[message.from_user.id] = 2


@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 2)
def middle_name(message):
    UserData.objects(user_id=message.from_user.id).update(middle_name=message.text)
    bot.send_message(message.chat.id, 'Enter your phone:')
    user_step[message.from_user.id] = 3


@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 3)
def phone(message):
    UserData.objects(user_id=message.from_user.id).update(phone=message.text)
    bot.send_message(message.chat.id, 'Enter your email:')
    user_step[message.from_user.id] = 4


@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 4)
def email(message):
    UserData.objects(user_id=message.from_user.id).update(email=message.text)
    bot.send_message(message.chat.id, 'Enter your address:')
    user_step[message.from_user.id] = 5


@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 5)
def address(message):
    UserData.objects(user_id=message.from_user.id).update(address=message.text)
    bot.send_message(message.chat.id, 'Enter your wishes:')
    user_step[message.from_user.id] = 6


@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 6)
def wishes(message):
    UserData.objects(user_id=message.from_user.id).update(wishes=message.text)
    bot.send_message(message.chat.id, 'Registration successful!')
    user_step[message.from_user.id] = 0


bot.polling(none_stop=True)












































# data = {
#
#         'name': None,
#         'surname': None,
#         'middle_name': None,
#         'phone': None,
#         'email': None,
#         'address': None,
#         'wishes': None
#
#         }
#
#
# def register():
#
#     if None in data.values():
#         return True
#
#     return False
#
#
# def beautiful_data(**kwargs):
#
#     beautiful_string = []
#
#     for key, value in kwargs.items():
#         beautiful_string.append(key.replace('_', ''))
#         beautiful_string.append(f' -- {value}\n')
#
#     return ''.join(beautiful_string)

# @bot.message_handler(func=lambda message: True if register() else False)
# def reg(message):
#
#     for key in data.keys():
#
#         if data[key] is None:
#             data[key] = message.message_id
#             bot.send_message(message.chat.id, f'{message.message_id.text}')
#             break
#
#     for key in data.keys():
#
#         if data[key] is None:
#             bot.send_message(message.chat.id, f'Input your {key}:')
#             break
#
#     if None not in data.values():
#         UserData(**data).save()
#         bot.send_message(message.chat.id, beautiful_data(**data))
#
#