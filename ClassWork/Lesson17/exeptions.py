class CostumeStringLengthException(Exception):

    def __init__(self, message, error):
        self._message = message
        self._error = error
        super().__init__()

    @property
    def message(self):
        return self._message

    @property
    def error(self):
        return self._error

    def __str__(self):
        return self._message, self._error

def input_str(string: str):

    if len(string) < 1:
        raise CostumeStringLengthException('Len must be more then 1',
                                           'EmptyStringException')



try:

    input_str('')

except CostumeStringLengthException as e:
    print(e)
