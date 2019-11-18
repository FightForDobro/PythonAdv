import models.models as db

# ******************************** Перечеркнутый текст ********************************


def strike(text):
    result = ''
    for c in text:
        result = result + c + '\u0336'
    return result

# *************************************************************************************

# ******************************** Получить текущую цену ******************************


def get_price(product):

    if product.is_discount:
        return product.new_price, strike(str(product.price))

    return product.price, product.price
# *************************************************************************************

# ******************* Получить стоимосте всех товаро в корзине ************************


def get_cart_price(cart):

    price = 0

    for i in cart.all_products:

        if i.is_discount:
            price += i.new_price

        elif not i.is_discount:
            price += i.price

        else:
            print(f'Error no such price or product\n'
                  f'Product id: {i.id}')

    return price

# *************************************************************************************
