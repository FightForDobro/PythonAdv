class CostumeList:

    def __init__(self, *args):
        self._costume_list = list(args)

    def append(self, value):
        self._costume_list = self._costume_list + [value]

    def pop(self, index):

        if index >= len(self._costume_list):
            raise IndexError(f'{index} index out of range\n'
                             f'Possible index {len(self._costume_list) - len(self._costume_list)} '
                             f'to {len(self._costume_list) - 1}')

        temp_value = self._costume_list[index]

        del self._costume_list[index]
        return temp_value

    def remove(self, value):

        if value not in self._costume_list:
            raise ValueError(f'{value} not in list')

        del self._costume_list[self._costume_list.index(value)]

    def insert(self, index, value):

        if index >= len(self._costume_list):
            raise IndexError(f'{index} index out of range\n'
                             f'Possible index {len(self._costume_list) - len(self._costume_list)} '
                             f'to {len(self._costume_list) - 1}')

        self._costume_list = self._costume_list[:index] + [value] + self._costume_list[index:]

    def clear(self):

        self._costume_list = []

    def get_list(self):

        return self._costume_list

    def __add__(self, other):
        return self._costume_list + other.get_list()

    def __str__(self):
        return str(self._costume_list)


a = CostumeList(1, 2, 3, 4, 5, 6)
b = CostumeList(1, 5, 6, 7, 8, 3)
c = a + b
print(c)
# a.append(5)
# a.insert(3, 99)
# print(a)
# a.clear()
# print(a)


class CostumeDict:

    def __init__(self, **kwargs):
        self._costume_dict = kwargs

    def get(self, key, default=0):

        if key not in self._costume_dict:
            return default

        else:
            return self._costume_dict[key]

    def items(self):

        items = []

        for key in self._costume_dict:
            items.append((key, self._costume_dict[key]))

        return items

    def keys(self):

        keys = []

        for key in self._costume_dict:
            keys.append(key)

        return keys

    def values(self):

        values = []

        for key in self._costume_dict:
            values.append(self._costume_dict[key])

        return values

    def __add__(self, other):

        for key, value in other.items():
            self._costume_dict[key] = value

        return self._costume_dict

    def __str__(self):
        return str(self._costume_dict)


a = CostumeDict(**{'a': 1, 'b': 2, 'c': 3})  # НЕЗАБИВАЙ РАСПАКОВИВАТЬ
b = CostumeDict(**{'f': 1, 'g': 2, 'd': 3})

a + b

print(a)
