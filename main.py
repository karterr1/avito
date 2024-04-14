import datetime
from flask import Flask, render_template, url_for, jsonify, make_response, request, redirect
from flask_restful import reqparse, abort, Api, Resource
from data import db_session
from data.users_resources import UsersResource, UsersListResources
from forms.login_form import LoginForm
from forms.register_form import RegForm
from forms.adverts_form import AdvertForm
from os.path import join, normpath
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data.user import Users
from data.adverts import Advert
import config

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDERS
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(Users).get(user_id)


@app.route('/')
def index():
    photo = [["/static/img/one.PNG", "/static/img/two.PNG", "/static/img/one.PNG", "/static/img/two.PNG"],
             ["/static/img/one.PNG", "/static/img/two.PNG", "/static/img/one.PNG", "/static/img/two.PNG"],
             ["/static/img/one.PNG", "/static/img/two.PNG"]]
    return render_template('index.html', title='Вы тут найдете всё', photos=photo)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(Users).filter(Users.email == form.email.data).first():
            return render_template('registration.html', title='Регистрация', form=form, message='такая почта уже есть')
        if db_sess.query(Users).filter(Users.login == form.login.data).first():
            return render_template('registration.html', title='Регистрация', form=form, message='такой логин уже есть')
        if form.password.data != form.password_again.data:
            return render_template('registration.html', title='Регистрация', form=form, message='пароли не совпадают')
        if request.files['file']:
            file = request.files['file']
            filename = secure_filename(file.filename)
            path = normpath(join(app.config['UPLOAD_FOLDER']['PROFILE_IMAGES_FOLDER'], filename))
            file.save(path)
        else:
            path = join(app.config['UPLOAD_FOLDER']['PROFILE_IMAGES_FOLDER'], 'default_image.png')
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
        return redirect('/')
    return render_template('registration.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(Users).filter(Users.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', form=form, title='Авторизация')


@app.route('/profile/<int:id>')
def profile(id):
    session = db_session.create_session()
    user = session.query(Users).filter(Users.id == id).first()
    print(user.photo)
    return render_template('profile.html', title='Профиль', user=user)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.route('/add', methods=['GET', 'POST'])
def add_adverts():
    form = AdvertForm()
    if form.validate_on_submit():
        print('ale')
        db_sess = db_session.create_session()
        ad = Advert(
            title=form.title.data,
            city=form.city.data,
            phone_number=form.phone_number.data,
            address=form.address.data
        )
        db_sess.add(ad)
        db_sess.commit()
        return redirect('/')
    return render_template('adverts_add.html', title='Объявление', form=form)


@app.errorhandler(401)
def unauthorized(_):
    return redirect('/login')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/avito_db.db")
    api.add_resource(UsersResource, '/api/users/<int:users_id>')
    api.add_resource(UsersListResources, '/api/users')
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
