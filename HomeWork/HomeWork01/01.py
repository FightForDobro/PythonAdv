class DataType:

    def __init__(self, collection=None):
        if collection is None:
            collection = []
        self._collection = collection

    def get(self):

        if self.is_empty():
            return print('List is empty')

        print(self._collection[-1])
        del self._collection[-1]

    def clean(self):

        del self._collection[0:]

    def is_empty(self):

        return not self._collection


class Stack(DataType):

    def __init__(self, stack=None):
        super().__init__(stack)

    def add(self, value):

        self._collection += [value]


class Queue(DataType):

    def __init__(self, queue=None):
        super().__init__(queue[::-1])

    def add(self, value):

        self._collection = [value] + self._collection


stack = Stack([1, 2, 3])
stack.add(5)
stack.get()
stack.get()
stack.get()
stack.get()
print('---')
queue = Queue([1, 2, 3])
queue.add(5)
queue.get()
queue.get()
queue.get()
queue.get()