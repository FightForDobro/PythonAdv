import telebot
import PythonAdv.PythonAdv.ClassWork.Lesson11.config as config
from telebot.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

bot = telebot.TeleBot(config.TOKEN)

data = []


@bot.message_handler(commands=['start'])
def start(message):

    bot.send_message(message.chat.id, 'Hello im bot and i need your data :(+)')


@bot.message_handler(commands=['fullname'])
def fullname(message):

    bot.send_message(message.chat.id, 'Input your full name')

    data.append(message.text)



bot.polling(none_stop=True)

