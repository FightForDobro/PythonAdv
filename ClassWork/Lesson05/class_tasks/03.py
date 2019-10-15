class ContextManager:
    """
    Simple context manager
    """

    def __init__(self, file, flag='a'):
        """
        Function construct file
        :param file: file name
        :param flag: file mode
        "r" - Read - Default value. Opens a file for reading, error if the file does not exist
        "a" - Append - Opens a file for appending, creates the file if it does not exist
        "w" - Write - Opens a file for writing, creates the file if it does not exist
        "x" - Create - Creates the specified file, returns an error if the file exist
        "t" - Text - Default value. Text mode
        "b" - Binary - Binary mode (e.g. images)
        """
        self._file = open(file, flag)

    def __enter__(self):
        print('You are in Context Manager')
        print(f'Working with file: {self._file.name}')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Exit Context Manager')
        self._file.close()
        print(f'File closed')

    def read_file(self):
        return self._file.readlines()

    def write_file(self, usr_input):
        self._file.write(usr_input)


with ContextManager('some_file.txt', 'r') as some_file:
    print(some_file.read_file())

