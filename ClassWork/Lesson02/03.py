class Dots:

    AXES = {
            0: 'x',
            1: 'y',
            2: 'z'
    }

    def __init__(self, f_coordinates, s_coordinates):

        self._first_cords = f_coordinates
        self._second_cords = s_coordinates

    def get_coordinates(self, which, coordinate=-1):
        """
        Function prints chosen coordinates
        :param which: Choose between 1 or 2 coordinate
        :param coordinate: If left blank print x,y,z else print chosen coordinate
        :type which: int
        :type coordinate: int
        :return: Print current value of coordinate
        :rtype: str
        """

        coord = self.choose_axe(which)

        if coordinate >= 0 <= 2:
            return f'{Dots.AXES[coordinate]} is: {coord[coordinate]}'

        return f'x is: {coord[0]}\ny is: {coord[1]}\nz is: {coord[2]}'

    def set_coordinate_value(self, which, coordinate, value):
        """
        Function set value to coordinate
        :param which: Choose between 1 or 2 coordinate
        :param coordinate: Choose which coordinate going be changed
        :param value: Value which you want set
        :type which: int
        :type coordinate: int
        :type value: int
        :return: Nothing
        """

        coord = self.choose_axe(which)

        coord[coordinate] = value

    def choose_axe(self, which):
        """
        Function choose axe
        :param which: Number of coordinate
        :type which: int
        :return: Chosen coordinate var
        """

        if which == 1:
            return self._first_cords
        else:
            return self._second_cords

    def __add__(self, other):

        return self._first_cords[0] + self._second_cords[0], self._first_cords[1] + self._second_cords[1], \
               self._first_cords[2] + self._second_cords[2]

    def __sub__(self, other):

        return self._first_cords[0] - self._second_cords[0], self._first_cords[1] - self._second_cords[1], \
               self._first_cords[2] - self._second_cords[2]

    def __mul__(self, other):

        return self._first_cords[0] * self._second_cords[0], self._first_cords[1] * self._second_cords[1], \
               self._first_cords[2] * self._second_cords[2]

    def __idiv__(self, other):

        try:

            return self._first_cords[0] / self._second_cords[0], self._first_cords[1] / self._second_cords[1], \
                self._first_cords[2] / self._second_cords[2]

        except ZeroDivisionError:
            print('You cant divide by zero')


f_coord = [1, 2, 3]
s_coord = [4, 6, 1]
a = Dots(f_coord, s_coord)

print(a.get_coordinates(2))
print(a.__mul__(a))
print(a.get_coordinates(2))
