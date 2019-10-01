class Vehicle:

    NUM_OF_DOORS = 4
    FUEL_TYPE = 'Petrol'

    def move(self):
        print('Car moving')

    def set_fuel(self, value):
        self._fuel += value

    def get_fuel(self):
        return self._fuel

    def get_brand(self):
        return self._brand

    def set_brand(self, value):
        self._brand = value

    def get_engine(self):
        return self._engine

    def set_engine(self, value):
        self._engine = value


class Car(Vehicle):

    def __init__(self, brand, engine):
        self._brand = brand
        self._engine = engine
        self._fuel = 0

    def move(self):
        print('Move speed is: 278 km/h')
        print(f'{self._brand} move so fast Vzhyyyyyyy!')

    def __str__(self):
        return f'Brand is {self._brand} and engine is {self._engine}'


class HeavyCar(Vehicle):

    def __init__(self, brand, engine, max_carry_weight):
        self._brand = brand
        self._engine = engine
        self._max_carry_weight = max_carry_weight
        self._point = False

    def move(self):
        print(f'Truck {self._brand} with engine {self._engine} and max carry weight {self._max_carry_weight}')
        print(f'Moving to point ---> {self._point or "No point!"} ')

    def set_point(self, point):
        self._point = point

    def __str__(self):
        return f'Current truck is {self._brand} with engine {self._engine} and max carry weight {self._max_carry_weight}'


mb = HeavyCar('Mercedes-Benz', 'V6', '5000 Kg')
mb.set_point('Kiev')

mb.move()
