import telebot
from telebot.types import (
    InlineKeyboardButton,
)

from keyboards import ReplyKB, InlineKB
import config
import keyboards
from models import models as db
# from models.models import UserMenuCounter as user_pos
from utils.scripts import strike, get_cart_price, get_price, phone_validate
from utils.cron import cron_decorator
from flask import Flask, request, abort
from datetime import timedelta


app = Flask(__name__)
bot = telebot.TeleBot(config.TOKEN)


# Process webhook calls
@app.route('/', methods=['POST'])
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
        db.User.create_user(str(message.chat.id), f'{message.chat.last_name}',
                            f'{message.chat.first_name}',
                            message.chat.username)

    db.User.objects(user_id=str(message.chat.id)).get().update(**{'active': True})

    greeting_str = 'Добро пожаловать в виртуальный мир BEATLEX'
    keyboard = ReplyKB().generate_kb(*keyboards.beginning_kb.values())
    keyboard.add('Личный кабинет')

    bot.send_message(message.chat.id, greeting_str, reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == 'Корзина')
def show_cart(message):

    user = db.User.objects(user_id=str(message.chat.id)).get()
    cart = db.Cart.objects(owner=user).get()

    bot.send_message(message.chat.id, 'CART',
                     reply_markup=InlineKB().generate_cart_kb(cart))


@bot.message_handler(func=lambda message: message.text == 'Личный кабинет')
def personal_account(message):
    keyboard = InlineKB().generate_pa(message.chat.id)

    bot.send_message(message.chat.id, 'Личный Кабинет',
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'add')
def edit_user_info(call):
    print(call.data)
    user = db.User.objects(user_id=str(call.message.chat.id)).get()

    if call.data.split('_')[1] == 'phone':  # TODO Добавить верификацю с смс
        bot.send_message(call.message.chat.id, 'Ведтие ваш номер телефона:')

        @bot.message_handler(func=phone_validate)
        def add_phone(message):
            user.update(**{'phone': message.text})
            bot.send_message(message.chat.id, 'Спасибо ваш номер добавлен')


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'help')
def popup_cart_help(call):
    definition_help = {
        'Название': 'Нажмите на названия чтобы вывести карту продукта',
        'Цена': 'Нажмите на цену чтобы вывести старую цену продукта',
        'Удалить': 'Нажмите на красный знакчок чтобы удалить товар с корзины',
        'cart': 'Это общая цена всех товаров в корзине',  # TODO Попробовать добавить общую цену без скидок
        'product': 'Здесь указано ваще текущее положение нажимайте кнопки < или > для перемещения',
        'empty': 'Здесь нет товара',
        'login': 'Здесь ваш логин',
        'fullname': 'Здесь ваше имя в телеграмм',
        'phone': 'Здесь ваш телефон'
    }

    bot.answer_callback_query(callback_query_id=call.id,
                              show_alert=True,
                              text=f'HELP:\n'
                                   f'{definition_help[call.data.split("_")[1]]}')


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'del')
def delete_product_from_cart(call):
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
    bot.answer_callback_query(callback_query_id=call.id,
                              show_alert=True,
                              text=f'Цена без скидки {call.data.split("_")[1]}')


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'buy')
def buy_cart(call):  # FIXME Перенести в скрипиться подумать над выводом в листе

    cart = db.Cart.objects(id=call.data.split('_')[1]).get()

    db.OrderHistory(**{'cart': cart.all_products,
                       'full_price': get_cart_price(cart),
                       'owner': cart.owner}).save()

    cart.update(set__all_products=[])

    bot.send_message(call.message.chat.id, 'Спасибо за покупку :)')


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'carthistory')
def show_order_history(call):
    keyboard = InlineKB().generate_order_history_kb(call.message.chat.id)

    bot.send_message(call.message.chat.id, 'История покупок',
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'history')
def show_old_cart(call):
    cart_id = call.data.split('_')[1]

    if not InlineKB().generate_swipe(int(call.data.split('_')[2]), cart_id):
        bot.answer_callback_query(call.id, 'Больше нет товаров', show_alert=True)
        return

    # user = db.User.objects(user_id=str(call.message.chat.id)).get()
    cart = db.OrderHistory.objects(id=cart_id).get()
    # product = db.Product.objects(id=cart.cart).get()

    p = cart.cart[int(call.data.split('_')[2])]

    print(call.data.split('_')[2])

    bot.send_photo(call.message.chat.id, p.img, caption=f'Вы вибрали продукт {p.title} \n\n'
                                                        f'Описание: \n'
                                                        f'{p.description} \n\n'
                                                        f'Цена: {get_price(p, for_print=True)}',
                   reply_markup=InlineKB().generate_swipe(int(call.data.split('_')[2]), cart_id)
                   )

    # bot.send_photo(call.message.chat.id, p.img, caption=f'Вы вибрали продукт {p.title} \n\n'
    #                                                           f'Описание: \n'
    #                                                           f'{p.description} \n\n'
    #                                                           f'Цена: {get_price(p, for_print=True)}',
    #                reply_markup=InlineKB().generate_swipe(int(call.data.split('_')[2]), call.message.chat.id),
    #                parse_mode='HTML')


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
    user = db.User.objects(user_id=str(call.message.chat.id)).get()

    db.UserMenuCounter.objects(owner=user).update(counter=0)

    if category.is_parent:

        keyboard = InlineKB().generate_kb(**{f'category_{d.id}': d.title for d in category.subcategory})

        keyboard.add(InlineKeyboardButton(text=f'<< {category.title}', callback_data=f'back_{category.id}'))

        # bot.edit_message_text(text=category.title, chat_id=call.message.chat.id,
        #                       message_id=call.message.message_id,
        #                       reply_markup=keyboard)

    else:

        print(' ----------------------------------------- TEST ----------------------------------------- ')

        # FIXME Проверить как работает код
        print(len(db.Product.objects(category=category)))
        print(db.Product.objects(category=category))

        keyboard = InlineKB().generate_products_buttons(call.message.chat.id, category, 6)

    bot.edit_message_text(text=category.title, chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'product')
def show_product(call):
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


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] in ['left', 'right'])
def swipe(call):
    user = db.User.objects(user_id=str(call.message.chat.id)).get()
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


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'back')
def go_back(call):
    if call.data.split('_')[1] == 'delete':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        return

    obj_id = call.data.split('_')[1]
    category = db.Category.objects(id=obj_id).get()

    if category.is_root:

        keyboard = InlineKB().generate_kb(
            **{f'category_{d.id}': d.title for d in db.Category.get_root_categories()})  # FIXME Исправить как ан уроке

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
    user = db.User.objects(user_id=str(call.message.chat.id)).get()

    if not db.Cart.objects(owner=user):
        user.create_cart()

    product = db.Product.objects(id=call.data.split('_')[1]).get()
    user.update_cart(product)


@bot.message_handler(func=lambda message: message.text == 'Продуккти со скидкой')
def show_sales_products(message):
    products = db.Product.get_discount_product()

    keyboard = InlineKB().generate_kb(
        **{f'product_{d.id}': d.title for d in products})  # TODO Добавить кнопку назад

    bot.send_message(text='Скидки', chat_id=message.chat.id,
                     reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == 'Информации о магазине')
def show_info(message):
    bot.send_message(message.chat.id, db.Texts.objects.first().title)
    bot.send_message(message.chat.id, db.Texts.objects.first().body)


@cron_decorator
def check_user_status(wait_time):
    try:

        for u in db.User.objects:

            while True:
                bot.send_chat_action(157301758, 'typing')

    except telebot.apihelper.ApiException:

        db.User.objects(user_id=u.user_id).get().update(**{'active': False})


if __name__ == '__main__':
    import time

    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(config.WEBHOOK_URL,
                     certificate=open('webhook_cert.pem', 'r'))
    check_user_status(int(timedelta(seconds=1).total_seconds()))
#   bot.polling(none_stop=True)
    app.run(debug=True)

