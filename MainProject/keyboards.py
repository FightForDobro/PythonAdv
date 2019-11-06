beginning_kb = {
    'news': 'Последние новости',
    'products': 'Продукти',
    'sales': 'Продуккти со скидкой',
    'about': 'Информации о магазине'
}


from telebot.types import (
    ReplyKeyboardMarkup,
    KeyboardButton
)


class ReplyKB(ReplyKeyboardMarkup):

    def __init__(self, one_time_keyboard=True, resize_keyboard=True, row_width=3):
        super().__init__(one_time_keyboard=one_time_keyboard,
                         resize_keyboard=resize_keyboard,
                         row_width=row_width)

    def generate_kb(self, *args):
        """
        :param args: Buttons names
        :return:
        """

        buttons = [KeyboardButton(b) for b in args]
        self.add(*buttons)
        return self

