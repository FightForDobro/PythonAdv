beginning_kb = {
    'news': 'Последние новости',
    'products': 'Продукти',
    'sales': 'Продуккти со скидкой',
    'about': 'Информации о магазине'
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

    def __init__(self, row_width=3):
        super().__init__(row_width=row_width)

    def generate_kb(self, *args, **kwargs):
        """
        :param args: Buttons names
        :param kwargs: Button names with specific callback_data
        """

        buttons = [InlineKeyboardButton(b, callback_data=b) for b in args]

        if kwargs:

            k_buttons = [InlineKeyboardButton(b, callback_data=d) for d, b in kwargs.items()]

            self.add(buttons + k_buttons)

        self.add(*buttons)

        return self

