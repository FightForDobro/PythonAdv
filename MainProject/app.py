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

from utils.scripts import strike

from flask import Flask, request, abort

app = Flask(__name__)
bot = telebot.TeleBot(config.TOKEN)


# Process webhook calls
@app.route(config.HANDEL_URL, methods=['POST'])
def webhook():

    if request.headers.get('content-type') == 'application/json':

        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''

    else:
        abort(403)


@bot.message_handler(commands=['start'])
def start(message):

    if not db.User.objects(user_id=str(message.chat.id)):

        db.User.create_user(str(message.chat.id), f'{message.chat.last_name} '
                                                  f'{message.chat.first_name}',
                                                  message.chat.username)

    greeting_str = 'Добро пожаловать в виртуальный мир BEATLEX'
    keyboard = ReplyKB().generate_kb(*keyboards.beginning_kb.values())

    bot.send_message(message.chat.id, greeting_str, reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == 'Корзина')
def show_cart(message):

    user = db.User.objects(user_id=str(message.chat.id)).get()

    cart_list = []

    cart = db.Cart.objects(owner=user).get()

    price = 0

    for i in cart.all_products:

        if i.is_discount:
            i.price = i.new_price

        cart_list.append(f'---------------------- \n'  # FIXME Добавить лен для палочек чтобы по размеру было 
                         f'Название: {i.title} \n'
                         f'Цена: {i.price} \n')  # FIXME Добавить проверки на скидку

        price += i.price

    keyboard = InlineKB().generate_kb(**{f'buy_{cart.id}_{price}': f'Купить: {price}'})  # FIXME Поулчать адекватно цену

    bot.send_message(message.chat.id, ''.join(cart_list),
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'buy')
def buy_cart(call):  # FIXME Перенести в скрипиться подумать над выводом в листе

    cart = db.Cart.objects(id=call.data.split('_')[1]).get()

    db.OrderHistory(**{'cart': cart.all_products,
                       'full_price': call.data.split('_')[2],
                       'owner': cart.owner}).save()

    cart.all_products = []

    bot.send_message(call.message.chat.id, 'Спасибо за покупку :)')


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

        keyboard.add(InlineKeyboardButton(text=f'<< {category.title}', callback_data=f'back_{category.id}'))

        bot.edit_message_text(text=category.title, chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=keyboard)

    else:

        for _ in db.Product.objects(category=category):  # FIXME Проверить как работает код
            keyboard = InlineKB().generate_kb(
                **{f'product_{d.id}': d.title for d in db.Product.objects(category=category)})  # FIXME make less code

            keyboard.add(InlineKeyboardButton(text=f'<< {category.title}', callback_data=f'back_{category.id}'))

            bot.edit_message_text(text=category.title, chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'product')
def show_product(call):

    product = db.Product.objects(id=call.data.split('_')[1]).get()

    keyboard = InlineKB().generate_kb(**{f'cart_{product.id}': 'Добавить в корзину'})

    if product.is_discount:
        bot.send_photo(call.message.chat.id, product.img.read(), caption=f'Вы вибрали продукт {product.title} \n\n'
                                                                         f'Описание: \n'
                                                                         f'{product.description} \n\n'
                                                                         f'Цена: {strike(str(product.price))} '
                                                                         f'{product.new_price}',
                                                                         reply_markup=keyboard,
                                                                         parse_mode='HTML')

    else:
        bot.send_photo(call.message.chat.id, product.img.read(), caption=f'Вы вибрали продукт {product.title} \n\n'
                                                                         f'Описание: \n'
                                                                         f'{product.description} \n\n'
                                                                         f'Цена: <b>{product.price}</b>',
                                                                         reply_markup=keyboard,
                                                                         parse_mode='HTML')

    # bot.send_message(call.message.chat.id, f'Вы вибрали продукт {product.title} \n\n'
    #                                        f'Описание: \n'
    #                                        f'Здесь должно быть ваше изображение \n\n'
    #                                        f'{product.description} \n\n'
    #                                        f'Цена: <b>{product.price}</b>',
    #                  reply_markup=keyboard,
    #                  parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'back')
def go_back(call):

    obj_id = call.data.split('_')[1]
    category = db.Category.objects(id=obj_id).get()

    if category.is_root:

        keyboard = InlineKB().generate_kb(**{f'category_{d.id}': d.title for d in db.Category.get_root_categories()})  # FIXME Исправить как ан уроке

    else:

        keyboard = InlineKB().generate_kb(**{f'category_{d.id}': d.title for d in category.parent.subcategory})

        keyboard.add(InlineKeyboardButton(text=f'<< {category.parent.title}',
                                          callback_data=f'back_{category.parent.id}'))

    text = 'Категории' if not category.parent else category.parent.title
    bot.edit_message_text(text=text, chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'cart')
def add_to_cart(call):
    # user = db.User.objects(id=call.data.)
    # if not db.Cart.objects(owner=)
    product = db.Product.objects(id=call.data.split('_')[1]).get()
    user = db.User.objects(user_id=str(call.message.chat.id)).get()
    user.update_cart(product)


@bot.message_handler(func=lambda message: message.text == 'Продуккти со скидкой')
def show_sales_products(message):

    products = db.Product.get_discount_product()

    keyboard = InlineKB().generate_kb(
        **{f'product_{d.id}': d.title for d in products})  # FIXME make less code

        # keyboard.add(InlineKeyboardButton(text=f'<< ', callback_data=f'back_{category.id}'))

    bot.send_message(text='%%% Скидки %%%', chat_id=message.chat.id,
                          reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == 'Информации о магазине')
def show_info(message):

    bot.send_message(message.chat.id, db.Texts.objects.first().title)
    bot.send_message(message.chat.id, db.Texts.objects.first().body)


if __name__ == '__main__':
    import time
    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(config.WEBHOOK_URL)
    app.run(debug=True)
