import models.models as db
from utils.scripts import get_price, get_cart_price

from math import ceil

beginning_kb = {
    'news': 'Последние новости',
    'products': 'Продукти',
    'sales': 'Продуккти со скидкой',
    'about': 'Информации о магазине',
    'user_cart': 'Корзина'
}


from telebot.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


class ReplyKB(ReplyKeyboardMarkup):

    def __init__(self, one_time_keyboard=True, resize_keyboard=True, row_width=3):
        super().__init__(one_time_keyboard=one_time_keyboard,
                         resize_keyboard=resize_keyboard,
                         row_width=row_width)

    def generate_kb(self, *args):
        """
        :param args: Buttons names
        """

        buttons = [KeyboardButton(b) for b in args]
        self.add(*buttons)
        return self


class InlineKB(InlineKeyboardMarkup):

    queries = {
        'root': db.Category.get_root_categories()
    }

    def __init__(self, row_width=3, key=None):
        super().__init__(row_width=row_width)
        self._query = self.queries.get(key)

    def generate_kb(self, *args, **kwargs):  # FIXME Можно доавить сюда ключ
        """
        :param args: Buttons names
        :param kwargs: Button names with specific callback_data
        """

        buttons = [InlineKeyboardButton(str(b), callback_data=str(b)) for b in args]

        if kwargs:

            k_buttons = [InlineKeyboardButton(str(b), callback_data=str(d)) for d, b in kwargs.items()]

            self.add(*(buttons + k_buttons))

        self.add(*buttons)

        return self

    def generate_root_kb(self):

        self.generate_kb()

    def generate_cart_kb(self, cart):

        cross_icon = u'\u274C'  # Значок -- красный крестик

        # Базовые кнопки сверху

        templates = ['Название', 'Цена', 'Удалить']
        buttons = [(InlineKeyboardButton(str(b), callback_data=f'help_{b}')) for b in templates]
        self.add(*buttons)

        # ----------------------------------------------------------------------------

        # Генератор кнопок для корзины
        for p in cart.all_products:

            current_price = get_price(p)
            self.add(InlineKeyboardButton(text=p.title,
                                          callback_data=f'product_{p.id}'),
                     InlineKeyboardButton(text=current_price[0],
                                          callback_data=f'old_{current_price[1]}'),
                     InlineKeyboardButton(text=cross_icon,
                                          callback_data=f'del_{p.id}'))

        self.add(InlineKeyboardButton(text=f'Цена корзины: {get_cart_price(cart)}', callback_data='help_cart'))
        self.add(InlineKeyboardButton(text='Купить', callback_data=f'buy_{cart.id}'))

        return self
        # --------------------------------------------------------------------------

    def generate_products_buttons(self, user_id, category):

        user_id = str(user_id)
        user = db.User.objects(user_id=user_id).get()
        products = db.Product.objects(category=category)

        counter = {}

        if not db.UserMenuCounter.objects(owner=user):
            db.UserMenuCounter(**{'owner': user}).save()    

        counter.update({user_id: db.UserMenuCounter.objects(owner=user).get().counter})

        if counter[user_id] > len(products):

            counter[user_id] += len(products) % 6

        buttons = []

        while len(buttons) != 9:

            for i, p in enumerate(products[db.UserMenuCounter.objects(owner=user).get().counter::]):

                if len(buttons) == 9:
                    break

                if i <= 6:
                    buttons.append(InlineKeyboardButton(text=f'{p.title}',
                                                        callback_data=f'product_{p.id}'))
                    counter[str(user_id)] += 1

                if 6 > len(products[db.UserMenuCounter.objects(owner=user).get().counter::]) > i:

                    for _ in range(6 - len(products[db.UserMenuCounter.objects(owner=user).get().counter::])):
                        buttons.append(InlineKeyboardButton(text=' ', callback_data=f'help_empty'))
                        counter[str(user_id)] += 1

                if counter[str(user_id)] == db.UserMenuCounter.objects(owner=user).get().counter + 6:

                    db.UserMenuCounter.objects(owner=user).update(counter=counter[user_id])

                    buttons.append(InlineKeyboardButton(text=' < ', callback_data=f'sback_{user_id}_{category.title}'))
                    buttons.append(InlineKeyboardButton(text=f' {counter[user_id] // 6}/{ceil(len(products) / 6)} ',
                                                        callback_data=f'help_product'))
                    buttons.append(InlineKeyboardButton(text=' > ', callback_data=f'forward_{user_id}_{category.title}'))

        print(buttons)
        print(self)
        self.add(*buttons)
        self.add(InlineKeyboardButton(text=f'<< {category.title}', callback_data=f'back_{category.id}'))
        return self

# class InlineKBNew(InlineKeyboardMarkup):
#
#     def __init__(self, iterable, named_arg, lookup_field=id, title_field='title', row_width=3):
#         super().__init__(row_width=row_width)
#
#         self._iterable = iterable
#         self._named_arg = named_arg
#         self._lookup_field = lookup_field
#         self._title_field = title_field
#
#     def generate_kb(self):
#         buttons = []
#
#         for i in self._iterable:
#             buttons.append(InlineKeyboardButton(
#                 text=getattr(i, self._title_field),
#                 callback_data=f'{self._named_arg}_' + str(getattr(i, self._lookup_field))
#             ))
#
#         self.add(*buttons)
#         return self
