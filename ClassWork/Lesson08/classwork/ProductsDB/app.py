from flask import (
                    Flask,
                    render_template,
                    request
                  )
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('products.db')  # For context manager


@app.route('/')
def main_route():

    def get_category():

        try:

            with conn:

                query_response = conn.execute('''select category_title from category''')

                return [''.join(i) for i in query_response.fetchall()]

        except sqlite3.IntegrityError:
            print('Error')

    return render_template('index.html',
                           categorys=get_category())


if __name__ == '__main__':
    app.run(debug=True)
