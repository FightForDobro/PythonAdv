#######################################################################################################################
#       Iter ObJ
#######################################################################################################################
# list_a = [1, 2 , 3]
# iter_obj = iter(list_a)
# print(next(iter_obj))
#       Iter ObJ
#######################################################################################################################
#         SimpleIterator
#######################################################################################################################
# class SimpleIterator:
#
#     def __init__(self, start, end, step):
#         self._start = start
#         self._end = end
#         self._step = step
#
#     def __iter__(self):
#         return self
#
#     def __next__(self):
#
#         while self._start < self._end:
#             self._start += self._step
#             return self._start
#
#         raise StopIteration
#
#
# obj = SimpleIterator(0, 100, 1)
# iter_obj = iter(obj)
#
#
# for i in obj:
#     print(i)
#######################################################################################################################
#                                               GENERATOR & YIELD
#######################################################################################################################


# def generator_func(start, end, step):
#
#     while start < end:
#         start += step
#         yield start
#         yield 'I am generator'
#
#     raise StopIteration
#
#
# generator_expression = (x ** 2 for x in range(100))
#
# print(generator_expression)
#
# obj = generator_func(0, 10, 1)
# iter_obj = iter(obj)
# print(next(iter_obj))
# print(next(iter_obj))
# print(next(iter_obj))
# next(iter_obj)
# print(next(iter_obj))
# print(next(iter_obj))

#######################################################################################################################
#                                               Own DataType
#######################################################################################################################

# class Array(list):
#
#     TYPES = (int, str, float)
#
#     def __init__(self, size, def_value):        #
#         self._array = [def_value] * size        # elems = [def_val] * size
#                                                 # super().__init__(elems)
#     def __setitem__(self, key, value):
#
#         if isinstance(value, Array.TYPES) and key <= len(self) - 1:
#             self._array[key] = value
#             return
#
#         raise ValueError('Out of Range')
#
#     def __getitem__(self, item):
#         if isinstance(item, int) and item <= len(self) - 1:
#             return self._array[item]
#
#         raise ValueError('Out of Range')
#
#     def __str__(self):
#
#         return str(self._array)
#
#     def __len__(self):
#         return len(self._array)
#
#
# array = Array(100, None)
#
# array[99] = 12
# print(array[99])
# print(len(array))
