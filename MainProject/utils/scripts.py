import models.models as db

# ******************************** Перечеркнутый текст ********************************


def strike(text):
    result = ''
    for c in text:
        result = result + c + '\u0336'
    return result

# *************************************************************************************

# ******************************** Получить текущую цену ******************************


def get_price(product, for_print=False):

    if product.is_discount:

        if not for_print:
            return product.new_price, strike(str(product.price))

        return f'{strike(str(product.price))} {product.new_price}'

    if not for_print:
        return product.price, product.price

    return product.price
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

# ************************* Валидация телефона ****************************************


def phone_validate(phone):

    phone = phone.text
    if '+' in phone:
        phone = phone.replace('+', '')

    if len(phone) == 12 or len(phone) == 9 and phone.isdigit():
        return True

    return False

# *************************************************************************************

# ************************* Валидация телефона ****************************************


def default_photo():

    with open('/home/ffd/Downloads/PythonAdv/MainProject/img/default.png', 'rb') as f:

        return f.read()

# *************************************************************************************
