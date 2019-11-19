# categories = {'VIDEO GAME': [
#     {'PC': {'Action': 'RPG'}},
#     {'XBox': ['Action', 'RPG', 'Strategy']},
#     {'PlayStation': ['Action', 'RPG', 'Strategy']}
# ]}


# def category_maker():
#
#     category_dict = {}
#
#     for root_c_t, root_c_v in categories.items():
#         for sub_c in root_c_v:
#             for k, v in sub_c.items():
#
#                 if type(v) is dict:
#                     root_c_v = v
#
#                 elif type(v) is list:
#
#                     for i in v:
#
#                         category_dict[root_c_t] = {k: i}
#
#                     break
#
#                 category_dict[root_c_t] = {k: v}
#
#     return category_dict

# class Test:
#
#     def __init__(self):
#         self._root_route = []
#
#     def category_digger(self, categories):
#
#         if type(categories) is list:
#
#             for i in categories:
#
#                 if type(i) is dict:
#
#                     for k, v in i.items():
#
#                         self._root_route.append(k)
#                         return self.category_digger(v)
#
#                 elif type(i) is str:
#                     print(i)
#
#         elif type(categories) is dict:
#
#             for k, v in categories.items():
#                 self._root_route.append(k)
#                 return self.category_digger(v)
#
#         elif type(categories) is str:
#             print(categories)

    # for root_category in test_dict:
    #     for sub_category in test_dict[root_category]:
    #
    #         if sub_category is dict:
    #             for subsub_category in sub_category:
    #
    #
    # return True

#
# test = category_digger()
# print(test)

# test = {}
#
# test['a'] = 'b'
# print(test)

# test_dict = {
#     'root_c': [
#
#         {
#             'PC': [
#                 {'Steam': ['Action', 'RPG', 'Strategy']},
#                 {'EpicGame': ['Battle Royal', 'Horror', 'Fight']},
#                 {'Uplay': 'Parkour'}
#             ]
#         },
#
#         {
#             'Xbox': ['Action', 'RPG', 'Strategy']
#         },
#
#         {
#             'PlayStation': ['Action', 'RPG', 'Strategy']
#         }
#     ]
# }


# for root_t, root_v in test_dict.items():
#     for sub_c in root_v:
#
#         if type(sub_c) is dict:
#
#             category_digger(sub_c)
#
#         elif type(sub_c) is list:
#             category_digger(sub_c)
#
#         elif type(sub_c) is str:
#             category_digger(sub_c)

# for i in test_dict:
#     category_digger(test_dict[i])

# Test().category_digger(test_dict)

































import telebot
import ast
import time
from telebot import types

bot = telebot.TeleBot("1016303038:AAF4ENbETYZQak6PHYfSA8hDFb8xLGwyzaQ")

stringList = {"Name": "John", "Language": "123456789012345678901234567890", "API": "pyTelegramBotAPI"}
crossIcon = u"\u274C"


def makeKeyboard():
    markup = types.InlineKeyboardMarkup()

    for key, value in stringList.items():
        markup.add(types.InlineKeyboardButton(text=value,
                                              callback_data="['value', '" + value + "', '" + key + "']"),
        types.InlineKeyboardButton(text=crossIcon,
                                   callback_data="['key', '" + key + "']"),
                   types.InlineKeyboardButton(text='X',
                                              callback_data='X'))

    return markup


@bot.message_handler(commands=['test'])
def handle_command_adminwindow(message):
    bot.send_message(chat_id=message.chat.id,
                     text="Here are the values of stringList",
                     reply_markup=makeKeyboard(),
                     parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):

    if (call.data.startswith("['value'")):
        print(f"call.data : {call.data} , type : {type(call.data)}")
        print(f"ast.literal_eval(call.data) : {ast.literal_eval(call.data)} , type : {type(ast.literal_eval(call.data))}")
        valueFromCallBack = ast.literal_eval(call.data)[1]
        keyFromCallBack = ast.literal_eval(call.data)[2]
        bot.answer_callback_query(callback_query_id=call.id,
                              show_alert=True,
                              text="You Clicked " + valueFromCallBack + " and key is " + keyFromCallBack)

    if (call.data.startswith("['key'")):
        keyFromCallBack = ast.literal_eval(call.data)[1]
        del stringList[keyFromCallBack]
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text="Here are the values of stringList",
                              message_id=call.message.message_id,
                              reply_markup=makeKeyboard(),
                              parse_mode='HTML')


while True:

    try:
        bot.polling(none_stop=True, interval=0, timeout=0)

    except:

        time.sleep(10)
