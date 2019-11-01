# TODO InlineQuery

import telebot
import config
from telebot.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)


bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def start(message):

    bot.send_message(message.chat.id, 'Hello')

    keyboard = ReplyKeyboardMarkup(
        one_time_keyboard=True,
        resize_keyboard=True
    )

    list_of_buttons = [KeyboardButton(f'Button-{k}') for k in range(6)]
    keyboard.add(*list_of_buttons)
    bot.send_message(message.chat.id, 'THE TEXT', reply_markup=keyboard)


@bot.message_handler(commands=['inline'])
def inline(message):
    keyboard = InlineKeyboardMarkup()
    buttons = [InlineKeyboardButton(f'InlineButton-{k}', callback_data=str(k)) for k in range(18)]
    keyboard.add(*buttons)
    bot.send_message(message.chat.id, 'Inline Mode', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_example(call):

    bot.send_message(call.message.chat.id,
                     f'I am message from inline mode the data is {call.data}')


@bot.message_handler(func=lambda message: message.text == 'Hi')
def echo(message):

    bot.send_message(message.chat.id,
                     'Hi, Hello!')


@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.send_message(message.chat.id,
                     message.text)


bot.polling(none_stop=True)
