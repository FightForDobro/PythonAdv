class Dot:

    AXES = {
            0: 'x',
            1: 'y',
            2: 'z'
    }

    def __init__(self, x, y, z):

        self._x = x
        self._y = y
        self._z = z

    def get_coordinates(self):
        """
        Function gets list of value
        :return: list of value
        :rtype: str
        """

        return list(self.__dict__.values())

    def set_coordinate_value(self, coordinate, value):
        """
        Function set value to coordinate
        :param coordinate: Choose which coordinate going be changed
        :param value: Value which you want set
        :type coordinate: str
        :type value: int
        :return: Nothing
        """
        coordinates = self.__dict__

        coordinate = f'_{coordinate}'

        if coordinate in coordinates.keys():

            self.__dict__[coordinate] = value

    def print_result(self):
        """
        Function prints pretty output
        :return: None
        """

        print(f'x: {self._x}\n'
              f'y: {self._y}\n'
              f'z: {self._z}\n')

    def __add__(self, other):

        return Dot(
            self.get_coordinates()[0] + other.get_coordinates()[0],
            self.get_coordinates()[1] + other.get_coordinates()[1],
            self.get_coordinates()[2] + other.get_coordinates()[2]
        )

    def __sub__(self, other):

        return Dot(
            self.get_coordinates()[0] - other.get_coordinates()[0],
            self.get_coordinates()[1] - other.get_coordinates()[1],
            self.get_coordinates()[2] - other.get_coordinates()[2]
        )

    def __mul__(self, other):

        return Dot(
            self.get_coordinates()[0] * other.get_coordinates()[0],
            self.get_coordinates()[1] * other.get_coordinates()[1],
            self.get_coordinates()[2] * other.get_coordinates()[2]
        )

    def __truediv__(self, other):

        try:

            return Dot(
                self.get_coordinates()[0] / other.get_coordinates()[0],
                self.get_coordinates()[1] / other.get_coordinates()[1],
                self.get_coordinates()[2] / other.get_coordinates()[2]
            )

        except ZeroDivisionError:
            print('You cant divide by zero')


f_coord = (2, 6, 2)
s_coord = (4, 3, 2)

a = Dot(*f_coord)
b = Dot(*s_coord)

c = a / b

c.print_result()

