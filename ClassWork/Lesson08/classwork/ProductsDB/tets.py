import sqlite3
import collections
conn = sqlite3.connect('products.db')


def get_category():

    try:

        with conn:

            query_response = conn.execute('''select * from category''')

            return dict(query_response.fetchall())

    except sqlite3.IntegrityError:
        print('Error')


def get_product_info():

    products = {c: {} for c in get_category()}

    try:

        with conn:

            query_response = conn.execute('''select * from products 
            inner join category c on products.category_id = c.id''')

            names = [name[0] for name in query_response.description]

            for value_list in query_response:

                result = product_dict(names, value_list)

                products[value_list[7]][value_list[1]] = result

            return products

    except sqlite3.IntegrityError:
        print('Error')


def product_dict(names, values):

    products_dict = {}
    for key, value in zip(names, values):

        if key == 'in_stock':
            products_dict[key] = bool(value)

        elif key == 'p_name':
            continue

        elif key == 'category_id':
            continue

        else:
            products_dict[key] = value

    return products_dict


# for i in get_product_info()['drinks'].keys():
#     print(i)

a = ['Potato', '1', '52', '1', '2']

print(list(map(lambda x: x if (str(x).isalpha()) else int(x), a)))



