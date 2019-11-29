import telebot
from telebot.types import (
    InlineKeyboardButton,
)

from keyboards import ReplyKB, InlineKB
import config
import keyboards
from models import models as db
from utils.scripts import get_cart_price, get_price, phone_validate
from utils.cron import cron_decorator
from flask import Flask, request, abort

app = Flask(__name__)
bot = telebot.TeleBot(config.TOKEN)


@app.route('/', methods=['POST'])
def webhook():
    """
    Function process webhook call
    """
    if request.headers.get('content-type') == 'application/json':

        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''

    else:
        abort(403)


# @bot.message_handler(commands=['test'])
# def test(message):
#
#     print(db.Product.objects(id='5ddace617971674a6aa8093c').get().f_img)
#     bot.send_photo(message.chat.id, db.Product.objects(id='5ddace617971674a6aa8093c').get().f_img, 'This is Product')


@bot.message_handler(commands=['start'])
def start(message):
    """
    First handler run on user first connection
    Adds new user to db
    Shows main keyboard
    Make user status active in order to check if user stop bot
    """

    if not db.User.objects(user_id=str(message.chat.id)):
        db.User.create_user(str(message.chat.id), f'{message.chat.last_name}',
                            f'{message.chat.first_name}',
                            message.chat.username)

    db.User.objects(user_id=str(message.chat.id)).get().update(**{'active': True})

    greeting_str = 'Добро пожаловать в виртуальный мир BEATLEX'
    keyboard = ReplyKB().generate_kb(*keyboards.beginning_kb.values())
    keyboard.add('Личный кабинет \U0001F468\U0001F3FC\U0000200D\U0001F4BB')

    bot.send_message(message.chat.id, greeting_str, reply_markup=keyboard)


@bot.message_handler(func=lambda message: 'Корзина' in message.text)
def show_cart(message):
    """
    Function show cart to user
    """

    user = db.User.objects(user_id=str(message.chat.id)).get()
    cart = db.Cart.objects(owner=user).get()

    bot.send_message(message.chat.id, 'Корзина \U0001F6D2',
                     reply_markup=InlineKB().generate_cart_kb(cart))


@bot.message_handler(func=lambda message: 'Личный кабинет' in message.text)
def personal_account(message):
    """
    Function show personal account
    :param message:
    :return:
    """
    keyboard = InlineKB().generate_pa(message.chat.id)

    bot.send_message(message.chat.id, f'Личный Кабинет \U0001F468\U0001F3FC\U0000200D\U0001F4BB',
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'add')
def edit_user_info(call):
    """
    Currently function allows to add/edit user mobile phone number
    But in future can be expanded for other editing options
    """

    user = db.User.objects(user_id=str(call.message.chat.id)).get()

    if call.data.split('_')[1] == 'phone':  # TODO Добавить верификацю с смс
        bot.send_message(call.message.chat.id, 'Ведтие ваш номер телефона:')

        @bot.message_handler(func=phone_validate)
        def add_phone(message):
            """
            Function update db and send message to user after completion
            Im think is beautiful to put that function here and allows to use variable user once
            """
            user.update(**{'phone': message.text})
            bot.send_message(message.chat.id, 'Спасибо ваш номер добавлен')


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'help')
def popup_help(call):
    """
    Function popup some useful notes to user
    all notes contains in db.Texts for simultaneously editing
    """
    bot.answer_callback_query(callback_query_id=call.id,
                              show_alert=True,
                              text=f'HELP:\n'
                                   f'{db.Texts.objects(title=call.data.split("_")[1]).get().body}')


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'del')
def delete_product_from_cart(call):
    """
    Function allows user to delete some product from cart dynamic
    """

    user = db.User.objects(user_id=str(call.message.chat.id)).get()
    cart = db.Cart.objects(owner=user).get()
    product = db.Product.objects(id=call.data.split('_')[1]).get()

    cart.update(pull__all_products=product.id)

    bot.edit_message_text(chat_id=call.message.chat.id,
                          text='CART',
                          message_id=call.message.message_id,
                          reply_markup=InlineKB().generate_cart_kb(db.Cart.objects(owner=user).get()))


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'old')
def popup_old_price(call):
    """
    Function popup old price
    """

    bot.answer_callback_query(callback_query_id=call.id,
                              show_alert=True,
                              text=f'Цена без скидки {call.data.split("_")[1]}')


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'buy')
def buy_cart(call):
    """
    Function allows user to buy cart
    """

    cart = db.Cart.objects(id=call.data.split('_')[1]).get()

    db.OrderHistory(**{'cart': cart.all_products,
                       'full_price': get_cart_price(cart),
                       'owner': cart.owner}).save()
    cart.update(set__all_products=[])

    bot.send_message(call.message.chat.id, 'Спасибо за покупку \n\n'
                                           'Приходите еще \U0001F3C3')


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'carthistory')
def show_order_history(call):
    """
    Function show user his order history
    """

    keyboard = InlineKB().generate_order_history_kb(call.message.chat.id)
    bot.send_message(call.message.chat.id, 'История покупок \U0001F6D2',
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'history')
def show_old_cart(call):
    """Function show user old cart"""

    cart_id = call.data.split('_')[1]

    if not InlineKB().generate_swipe(int(call.data.split('_')[2]), cart_id):
        bot.answer_callback_query(call.id, 'Больше нет товаров', show_alert=True)
        return

    cart = db.OrderHistory.objects(id=cart_id).get()
    p = cart.cart[int(call.data.split('_')[2])]  # call.data have such format 0 = call name
                                                                            # 1 = cart id
                                                                            # 2 = page count

    bot.send_photo(call.message.chat.id, p.img, caption=f'Вы вибрали продукт {p.title} \n\n'
                                                        f'Описание: \n'
                                                        f'{p.description} \n\n'
                                                        f'Цена: {get_price(p, for_print=True)}',
                   reply_markup=InlineKB().generate_swipe(int(call.data.split('_')[2]), cart_id)
                   )
    bot.delete_message(call.message.chat.id, call.message.message_id)


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] in ['left', 'right'])
def swipe(call):
    """
    Function makes swipe for product in old cart
    :param call:
    :return:
    """
    category = db.Category.objects(title=call.data.split('_')[2]).get()

    if call.data.split('_')[0] == 'left':

        keyboard = InlineKB().generate_products_buttons(call.message.chat.id, category, 6, back=True)

    elif call.data.split('_')[0] == 'right':
        keyboard = InlineKB().generate_products_buttons(call.message.chat.id, category, 6)

    if not keyboard:
        bot.answer_callback_query(callback_query_id=call.id,
                                  show_alert=True,
                                  text='ОШИБКА: \n'
                                       'Вы хотите переместиться на не существующую страницу!')

    else:
        bot.edit_message_text(text=category.title, chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=keyboard)


@bot.message_handler(func=lambda message: 'Последние новости' in message.text)
def show_news(message):
    """
    Function show up news
    """
    bot.send_message(message.chat.id, 'News')

    for i in db.News.objects:
        bot.send_message(message.chat.id, i.title)
        bot.send_message(message.chat.id, i.content)


@bot.message_handler(func=lambda message: 'Товары' in message.text)
def show_category(message):
    """Function show category"""

    keyboard = InlineKB().generate_kb(**{f'category_{d.id}': d.title for d in db.Category.get_root_categories()})
    bot.send_message(message.chat.id, 'MENU', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'category')
def show_product_or_subcategory(call):
    """
    Function show sub category or product menu
    :param call:
    :return: listed subcategories || listed products
    """

    obj_id = call.data.split('_')[1]
    category = db.Category.objects(id=obj_id).get()
    user = db.User.objects(user_id=str(call.message.chat.id)).get()

    db.UserMenuCounter.objects(owner=user).update(counter=0)

    if category.is_parent:

        keyboard = InlineKB().generate_kb(**{f'category_{d.id}': d.title for d in category.subcategory})

        keyboard.add(InlineKeyboardButton(text=f'<< {category.title}', callback_data=f'back_{category.id}'))

    else:

        keyboard = InlineKB().generate_products_buttons(call.message.chat.id, category, 6)

    bot.edit_message_text(text=category.title, chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'product')
def show_product(call):
    """
    Function show product page
    """

    product = db.Product.objects(id=call.data.split('_')[1]).get()
    category = product.category
    keyboard = InlineKB().generate_kb(**{f'cart_{product.id}': 'Добавить в корзину'})

    keyboard.add(InlineKeyboardButton(text=f'<< {category.title}', callback_data=f'back_{category.id}'))

    bot.send_photo(call.message.chat.id, product.img, caption=f'Вы вибрали продукт {product.title} \n\n'
                                                              f'Описание: \n'
                                                              f'{product.description} \n\n'
                                                              f'Цена: {get_price(product, for_print=True)}',
                   reply_markup=keyboard,
                   parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'back')
def go_back(call):
    """
    Back button logic
    """

    if call.data.split('_')[1] == 'delete':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        return

    obj_id = call.data.split('_')[1]
    category = db.Category.objects(id=obj_id).get()

    if category.is_root:

        keyboard = InlineKB().generate_kb(
            **{f'category_{d.id}': d.title for d in db.Category.get_root_categories()})

    else:

        keyboard = InlineKB().generate_kb(**{f'category_{d.id}': d.title for d in category.parent.subcategory})

        keyboard.add(InlineKeyboardButton(text=f'<< {category.parent.title}',
                                          callback_data=f'back_{category.parent.id}'))

    text = 'Категории' if not category.parent else category.parent.title

    try:

        bot.edit_message_text(text=text, chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=keyboard)

    except telebot.apihelper.ApiException:
        bot.delete_message(call.message.chat.id, call.message.message_id)


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'cart')
def add_to_cart(call):
    """
    Function add product to cart
    :param call:
    :return:
    """

    user = db.User.objects(user_id=str(call.message.chat.id)).get()
    product = db.Product.objects(id=call.data.split('_')[1]).get()

    if product in db.Cart.objects(owner=user).get().all_products:
        bot.answer_callback_query(call.id, f'{product.title} уже в корзине вы не можете доваить еще \U000026D4')
        return

    if not db.Cart.objects(owner=user):
        user.create_cart()

    user.update_cart(product)
    bot.answer_callback_query(call.id, f'{product.title} добавлен в корзину \U00002714\U0000FE0F', show_alert=True)


@bot.message_handler(func=lambda message: 'Товары со скидкой' in message.text)
def show_sales_products(message):
    """
    Function show products on sale
    """

    products = db.Product.get_discount_product()

    keyboard = InlineKB().generate_kb(
        **{f'product_{d.id}': d.title for d in products})  # TODO Добавить кнопку назад

    bot.send_message(text='Скидки', chat_id=message.chat.id,
                     reply_markup=keyboard)


@bot.message_handler(func=lambda message: 'Информации о магазине' in message.text)
def show_info(message):
    """
    Func prints Info about shop
    :param message:
    :return:
    """
    info = db.Texts.objects(category='info').get()

    bot.send_message(message.chat.id, info.title)
    bot.send_message(message.chat.id, info.body)


@cron_decorator
def check_user_status():
    """
    Function check whether user block bot or not
    """

    try:

        for u in db.User.objects:

            while True:
                bot.send_chat_action(u.user_id, 'typing')

    except telebot.apihelper.ApiException:

        db.User.objects(user_id=u.user_id).get().update(**{'active': False})


if __name__ == '__main__':
    import time

    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(config.WEBHOOK_URL,
                    certificate=open('webhook_cert.pem', 'r'))
    check_user_status()
    # bot.polling(none_stop=True)
    app.run(debug=True)

