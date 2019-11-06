from flask import (
                    Flask,
                    render_template,
                    request
                  )
from models import users as s_db


app = Flask(__name__)


@app.route('/')
def main_route():

    return render_template('index.html')


@app.route('/successful/<string:crud_status>', methods=['GET', 'POST'])
def successful(crud_status):

    if crud_status == 'create':
        s_db.Student.create_student(**dict(request.form))
        return render_template('successful.html')

    elif crud_status == 'read':
        student = s_db.Student.read_student(request.form['student_id'])[0]
        return render_template('successful.html',
                               student=dict(student))

    elif crud_status == 'update':

        new_data = dict(request.form)

        new_data = {k: v for k, v in new_data.items() if v}

        s_db.Student().update_student(**new_data)

        return render_template('successful.html')

    elif crud_status == 'delete':
        print(request.form['student_id'])
        s_db.Student.delete_student(request.form['student_id'])
        return render_template('successful.html')

    return 'ERROR'


@app.route('/generator/')
def generator_student():
    return s_db.add_some_students(100)


if __name__ == '__main__':
    app.run(debug=True)
