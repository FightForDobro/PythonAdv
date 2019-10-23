from flask import (
                    Flask,
                    render_template,
                    request
                  )

app = Flask(__name__)


@app.route('/get-student-info/<string:id>')
def hello_world(id):
    print(id)
    print(request.args)
    print(request.json)
    return 'Hello World!'


@app.route('/my-new-route/')
def my_route():

    users = {
        'Jonh': 'new_user',
        'Alex': 'new_user',
        'Jenny': 'old_user'
    }

    my_list = ['1', '2', '3', '4', '5']

    title = 'main_page'
    return render_template('index.html',
                           data='my_data',
                           title=title,
                           users=users,
                           template_list=my_list)


if __name__ == '__main__':
    app.run(debug=True)
