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

