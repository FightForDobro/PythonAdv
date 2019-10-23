class ComplexNumber:

    def __init__(self, a=0, b=0):
        """
        Function construct complex number
        :param a: real number
        :type a: Union[int, float]
        :type b: Union[int, float]
        :param b: imagine number
        """
        self._a = a
        self._b = b

    def get_a(self):
        """
        Function return real num
        """
        return self._a

    def get_b(self):
        """
        Function return real num
        """
        return self._b

    def __str__(self):
        """
        Function prints complex number in correct form
        :return: String
        :rtype: str
        """

        sign = ''
        if self.get_b() > 0:
            sign = '+'

        elif self.get_a() == self.get_b() or self.get_b() == 0:
            return f'z = {self.get_a()}i'

        elif self.get_a() == 0:
            return f'z = {self.get_b()}i'

        return f'z = {self.get_a()}{sign}{self.get_b()}i'

    def __add__(self, other):

        return ComplexNumber(
            self.get_a() + other.get_a(), self.get_b() + other.get_b()
        )

    def __sub__(self, other):

        return ComplexNumber(
            self.get_a() - other.get_a(), self.get_b() - other.get_b()
        )

    def __mul__(self, other):

        return ComplexNumber(
            self.get_a() * other.get_a() - self.get_b() * other.get_b(),
            self.get_b() * other.get_a() + self.get_a() * other.get_b()
        )

    def __truediv__(self, other):

        try:

            return ComplexNumber(
                (self.get_a() * other.get_a() + self.get_b() * other.get_b()) / ((other.get_a() ** 2) + (other.get_b() ** 2)),
                (self.get_b() * other.get_a() - self.get_a() * other.get_b()) / ((other.get_a() ** 2) + (other.get_b() ** 2)),
            )

        except ZeroDivisionError:
            exit(f'ERROR: {ZeroDivisionError.__name__}')


z1 = ComplexNumber(8, 4)
z2 = ComplexNumber(5, 5)

r = z1 / 4

print(r)
