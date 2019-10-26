# TODO Реорганизовать красиво код

from flask import (
                    Flask,
                    render_template,
                    request
                  )
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('products.db', check_same_thread=False)  # For context manager


@app.route('/')
def main_route():
    img_list = ['http://icons.iconarchive.com/icons/graphicloads/food-drink/256/drink-icon.png',
                'http://icons.iconarchive.com/icons/graphicloads/food-drink/256/catering-icon.png',
                'https://www.pinclipart.com/picdir/big/168-1681636_140-clothes-icon-packs-icon-t-shirt-png.png'
                ]
    return render_template('index.html',
                           categorys=get_category(),
                           imgs=img_list,
                           data=zip(get_category(), img_list))


@app.route('/product/<string:full_path>/')
def category_route(full_path):

    products = get_product_info()[full_path]

    print(products)
    return render_template('product.html',
                           products=products,
                           title=str(full_path).capitalize())


@app.route('/product/<string:full_path>/<string:product_name>', methods=['GET', 'POST'])
def product_route(full_path, product_name):

    products = get_product_info()[str(full_path).lower()][product_name]

    return render_template('singel_product.html',
                           title=str(product_name).capitalize(),
                           product=products,)


@app.route('/NOTADMINPANEL/', methods=['GET', 'POST'])
def admin_route():
    products = get_product_info()
    if dict(request.form) == get_admins():
        return render_template('admin.html',
                               categorys=get_category(True),
                               products=products)

    return login()


@app.route('/login/', methods=['GET', 'POST'])
def login():

    return render_template('login.html')


@app.route('/NOTADMINPANEL/additem/', methods=['GET', 'POST'])
def add_item():

    data = add_item_to_db(request.form)
    return render_template('successful.html',
                           data=data)


@app.route('/NOTADMINPANEL/edititem/', methods=['GET', 'POST'])
def edit_item():
    print(request.form)
    data = edit_item_in_db(request.form)
    return render_template('successful.html',
                           data=data)


def get_category(full=False):

    try:

        with conn:

            if full:

                query_response = conn.execute('''select * from category''')
                return dict(query_response.fetchall())

            else:
                query_response = conn.execute('''select category_title from category''')
                return [''.join(i) for i in query_response.fetchall()]

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

                print(value_list)
                products[value_list[8]][value_list[1]] = result

            return products

    except sqlite3.IntegrityError:
        print('Error')


def get_admins():

    try:

        with conn:

            query_response = conn.execute('''select login, pass from admins''')
            names = [name[0] for name in query_response.description]

            return product_dict(names, list(query_response)[0])

    except sqlite3.IntegrityError:
        print('Error')


def add_item_to_db(data):

    data = dict(data)

    try:

        with conn:

            data_to_sql = list(map(lambda x: x if not (str(x).isdigit()) else int(x), data.values()))

            conn.execute('''insert into 
            products(p_name, in_stock, number_of_units, price, img_link, category_id) 
            values (?, ?, ?, ?, ?, ?)''', data_to_sql)

            return data

    except sqlite3.IntegrityError:
        return 'Error'


def edit_item_in_db(data):

    data = dict(data)

    try:

        with conn:
            print(data)
            current_product = data.pop('c_p_name')
            data_to_sql = list(map(lambda x: x if not (str(x).isdigit()) else int(x), data.values()))

            conn.execute('''update products 
            set p_name=?, in_stock=?, number_of_units=?, category_id=?, price=?, img_link=?
            where p_name=?''', (*data_to_sql, current_product))
            return data
    except sqlite3.IntegrityError:
        return 'Error'


def product_dict(names, values):

    products_dict = {}
    for key, value in zip(names, values):

        if key == 'in_stock':
            products_dict[key.replace('_', ' ').title()] = bool(value)

        elif key == 'p_name':
            continue

        else:
            products_dict[key.replace('_', ' ').title()] = value

    return products_dict


if __name__ == '__main__':
    app.run(debug=True)
