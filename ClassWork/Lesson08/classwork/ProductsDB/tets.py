import sqlite3

conn = sqlite3.connect('products.db')


def get_category():

    try:

        with conn:

            query_response = conn.execute('''select category_title from category''')

            return [''.join(i) for i in query_response.fetchall()]

    except sqlite3.IntegrityError:
        print('Error')


print(get_category())

