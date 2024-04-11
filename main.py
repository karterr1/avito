import datetime

from flask import Flask, render_template, url_for, jsonify, make_response, request, redirect
from flask_restful import reqparse, abort, Api, Resource
from data import db_session
from data.users_resources import UsersResource, UsersListResources
from forms.login_form import LoginForm
from forms.register_form import RegForm
import os
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_user
from data.user import Users

UPLOAD_FOLDER = os.path.abspath('static/img')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(Users).get(user_id)


@app.route('/')
def index():
    photo = ["/static/img/one.PNG", "/static/img/two.PNG", "/static/img/one.PNG", "/static/img/two.PNG",
             "/static/img/one.PNG", "/static/img/two.PNG", "/static/img/one.PNG", "/static/img/two.PNG",
             "/static/img/one.PNG"]
    return render_template('chernovik.html', title='Вы тут найдете всё', photos=photo,
                           css1=url_for('static', filename='css/ww.css'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(Users).filter(Users.email == form.email.data).first():
            return render_template('registration.html', title='Регистрация', form=form, message='такая почта уже есть')
        if db_sess.query(Users).filter(Users.login == form.login.data).first():
            return render_template('registration.html', title='Регистрация', form=form, message='такой логин уже есть')
        if request.files['file']:
            file = request.files['file']
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
        else:
            path = os.path.join(app.config['UPLOAD_FOLDER'], 'default_image.png')
        user = Users(
            login=form.login.data,
            email=form.email.data,
            photo=path,
            created_date=datetime.datetime.now()
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user)
        return
    return render_template('registration.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    pass


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


def main():
    db_session.global_init("db/avito_db.db")
    api.add_resource(UsersResource, '/api/users/<int:users_id>')
    api.add_resource(UsersListResources, '/api/users')
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
