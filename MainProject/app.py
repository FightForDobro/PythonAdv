import telebot
from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButton,
    ReplyKeyboardMarkup
)

from keyboards import ReplyKB
import config
import keyboards
from models import models


bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def start(message):

    # greetings_str = models.Texts(title='Greetings').get().body
    greeting_str = 'Hi!'
    keyboard = ReplyKB().generate_kb(*keyboards.beginning_kb.values())
    bot.send_message(message.chat.id, greeting_str, reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.lower() == 'Последние новости'.lower())
def news(message):
    pass


@bot.message_handler(func=lambda message: message.lower() == 'Продукти'.lower())
def news(message):
    pass


@bot.message_handler(func=lambda message: message.lower() == 'Продуккти со скидкой'.lower())
def news(message):
    pass


@bot.message_handler(func=lambda message: message.lower() == 'Информации о магазине'.lower())
def news(message):
    pass


if __name__ == '__main__':
    bot.polling(none_stop=True)
