#TODO DATA_ART


from flask import (Flask,
                   request,
                   jsonify)

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello_world():

    if request.headers['auth_token'] == 'randomvalue':
        data = {'1': 2}
        return jsonify(data)

    else:
        return jsonify({'error_code': 'wrong_auth'})


if __name__ == '__main__':
    app.run(debug=True)
