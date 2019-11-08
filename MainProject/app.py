import telebot
from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButton,
    ReplyKeyboardMarkup
)

from MainProject.keyboards import ReplyKB, InlineKB
import MainProject.config as config
import MainProject.keyboards as keyboards
from MainProject.models import models as db


bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def start(message):

    # greetings_str = models.Texts(title='Greetings').get().body
    greeting_str = 'Hi!'
    keyboard = ReplyKB().generate_kb(*keyboards.beginning_kb.values())
    bot.send_message(message.chat.id, greeting_str, reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == 'Последние новости')
def news(message):

    bot.send_message(message.chat.id, 'News')

    for i in db.News.objects:

        bot.send_message(message.chat.id, i.title)
        bot.send_message(message.chat.id, i.content)


@bot.message_handler(func=lambda message: message.text == 'Продукти')
def news(message):

    keyboard = InlineKB().generate_kb(*[b.title for b in db.Category.objects])

    bot.send_message(message.chat.id, 'MENU', reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == 'Продуккти со скидкой')
def news(message):
    pass


@bot.message_handler(func=lambda message: message.text == 'Информации о магазине')
def news(message):

    bot.send_message(message.chat.id, db.Texts.objects.first().title)
    bot.send_message(message.chat.id, db.Texts.objects.first().body)


if __name__ == '__main__':
    bot.polling(none_stop=True)
