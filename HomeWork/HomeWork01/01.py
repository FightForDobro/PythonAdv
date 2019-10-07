class DataType:
    """
    Main class of Collection
    """

    def __init__(self, collection=None):
        """
        Function construct simple collection(list)
        :param collection: some list
        :type collection: list
        """
        if collection is None:
            collection = []
        self._collection = collection

    def get(self):
        """
        Get value from collection
        :return: None
        :rtype: None
        """

        self.is_empty()

        print(self._collection[-1])
        del self._collection[-1]

    def clean(self):
        """
        Clean collection
        """
        del self._collection[0:]

    def is_empty(self):
        """
        Checks if the collection is empty
        :return: Collection or exit
        """
        return self._collection or exit('Collection is Empty')


class Stack(DataType):

    def __init__(self, stack=None):
        """
        Construct stack
        :param stack: some list
        :type stack: list
        """
        super().__init__(stack)

    def add(self, value):
        """
        Add value to stack
        :param value: some numbers or symbols
        :type value: Union[int, str]
        """
        self._collection += [value]


class Queue(DataType):

    def __init__(self, queue=None):
        """
        Construct queue
        :param queue: some list
        :type queue: list
        """
        super().__init__(queue[::-1])

    def add(self, value):
        """
        Add value to queue
        :param value: some numbers or symbols
        :type value: Union[int, str]
        """
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
