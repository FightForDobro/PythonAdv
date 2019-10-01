class Shop:

    ALL_SALES = 0

    def __init__(self, name, sales=0):
        self._name = name
        self._sales = sales

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def add_sales(self, sales):
        self._sales += sales
        Shop.ALL_SALES += self._sales

    def get_sales(self):
        return self._sales

    def add_all_sales(self):
        Shop.ALL_SALES += self._sales


atb = Shop('ATB')
atb.get_name()
atb.set_name('ATB Premium')
atb.add_sales(100)

novus = Shop('Novus')
novus.add_sales(54)

silpo = Shop('Silpo')
silpo.add_sales(18)

print(f'All sales is: {Shop.ALL_SALES}')
