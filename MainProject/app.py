import telebot
from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButton,
    ReplyKeyboardMarkup
)

from keyboards import ReplyKB, InlineKB
import config
import keyboards
from models import models as db


bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def start(message):

    # greetings_str = models.Texts(title='Greetings').get().body
    greeting_str = 'Hi!'
    keyboard = ReplyKB().generate_kb(*keyboards.beginning_kb.values())
    bot.send_message(message.chat.id, greeting_str, reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == 'Последние новости')
def show_news(message):

    bot.send_message(message.chat.id, 'News')

    for i in db.News.objects:

        bot.send_message(message.chat.id, i.title)
        bot.send_message(message.chat.id, i.content)


@bot.message_handler(func=lambda message: message.text == 'Продукти')
def show_category(message):

    keyboard = InlineKB().generate_kb(**{f'category_{d.id}': d.title for d in db.Category.get_root_categories()})

    bot.send_message(message.chat.id, 'MENU', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'category')
def show_product_or_subcategory(call):

    """

    :param call:
    :return: listed subcategories || listed products
    """

    obj_id = call.data.split('_')[1]
    category = db.Category.objects(id=obj_id).get()

    if category.is_parent:

        keyboard = InlineKB().generate_kb(**{f'category_{d.id}': d.title for d in category.subcategory})
        bot.edit_message_text(text=category.title, chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=keyboard)

    else:

        for i in db.Product.objects(category=category):
            keyboard = InlineKB().generate_kb(**{f'product_{d.id}': d.title for d in db.Product.objects(category=category)})
            bot.edit_message_text(text=category.title, chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'product')
def show_product(call):

    product = db.Product.objects(id=call.data.split('_')[1]).get()

    keyboard = InlineKB().generate_kb(**{f'cart_{call.message.chat.id}': 'Добавить в корзину'})

    bot.send_message(call.message.chat.id, f'Вы вибрали продукт {product.title} \n\n'
                                           f'Описание: \n'
                                           f'Здесь должно быть ваше изображение \n\n'
                                           f'{product.description} \n\n'
                                           f'Цена: <del>{product.price}</del>',
                     reply_markup=keyboard,
                     parse_mode='HTML')


@bot.message_handler(func=lambda message: message.text == 'Продуккти со скидкой')
def show_sales_products(message):
    pass


@bot.message_handler(func=lambda message: message.text == 'Информации о магазине')
def show_info(message):

    bot.send_message(message.chat.id, db.Texts.objects.first().title)
    bot.send_message(message.chat.id, db.Texts.objects.first().body)


if __name__ == '__main__':
    bot.polling(none_stop=True)
