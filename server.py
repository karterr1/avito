import datetime
import os.path
from flask import Flask, render_template, url_for, jsonify, make_response, request, redirect
from flask_restful import Api
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
from data.adverts_images import AdvertsImages
from data.category import Category
import config
import pymorphy3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDERS
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
morph = pymorphy3.MorphAnalyzer()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(Users).get(user_id)


n = 0


@app.route('/', methods=['GET', 'POST'])  # обработчик главного экрана
def index():
    session = db_session.create_session()
    if request.method == 'POST':
        if request.form['query'].strip() in config.CATEGORIES:  # если пользователь ввел название одной из категорий
            id = session.query(Category).filter(Category.name == request.form['query'].strip()).first().id
            advert = session.query(Advert).filter(Advert.category_id == id).all()
        else:
            query_words = []  # поиск по объявлениям в базе данных
            advert = []
            for word in request.form['query'].split():
                parsed_word = morph.parse(word)[0]
                if 'NOUN' in parsed_word.tag or 'ADJF' in parsed_word.tag or 'VERB' in parsed_word.tag:
                    processed_word = parsed_word.inflect({'nomn'}).word
                    query_words.append(processed_word)
            adverts = session.query(Advert).all()
            for i in adverts:
                processed_words = []
                for word in i.title.split():
                    parsed_word = morph.parse(word)[0]
                    if 'NOUN' in parsed_word.tag or 'ADJF' in parsed_word.tag or 'VERB' in parsed_word.tag:
                        processed_word = parsed_word.inflect({'nomn'}).word

                        processed_words.append(processed_word)
                if set(processed_words).intersection(set(query_words)) or set(i.title.split()).intersection(
                        set(request.form['query'].split())):
                    advert.append(i)
    else:
        advert = session.query(Advert).all()
    smt = []
    photo = []
    photos = []
    n = 0
    for i in advert:  # получение изображений
        image = session.query(AdvertsImages).filter(AdvertsImages.advert_id == i.id).first()
        name = image.path, i.title, i.price, i.id
        smt.append(name)
    for i in range(1, len(smt) + 1):
        n += 1
        if n % 5 != 0:
            photo.append(smt[i - 1])
        else:
            photos.append(photo)
            photo = []
            photo.append(smt[i - 1])
            n = 1
        if i == len(smt):
            if n % 5 != 0:
                photos.append(photo)
            else:
                photos.append(smt[i - 1])
    return render_template('index.html', title='Вы тут найдете всё', photos=photos, photo=photo)


@app.route('/profile/<int:id>')  # обработчик профиля пользователя
def profile(id):
    images = []
    session = db_session.create_session()
    user = session.query(Users).filter(Users.id == id).first()
    adverts = session.query(Advert).filter(Advert.user_id == id)
    for i in adverts:
        image = session.query(AdvertsImages).filter(AdvertsImages.advert_id == i.id).first()
        n = i, image.path
        images.append(n)
    for i in images:
        photo = session.query(Users).all()
        return render_template('profile.html', title='Профиль', user=user, photos=photo, advert=images,
                               css1=url_for('static', filename='css/style_profile.css'))
    photo = session.query(Users).all()
    return render_template('profile.html', title='Профиль', user=user, photos=photo, advert=adverts,
                           css1=url_for('static', filename='css/style_profile.css'))


@app.route('/advert/<int:advert_id>', methods=['GET', 'POST'])
def advert(advert_id):  # окно с информацией про объявление
    session = db_session.create_session()
    advert = session.query(Advert).get(advert_id)
    user = session.query(Users).filter(Users.id == advert.user_id).first()
    photos = session.query(AdvertsImages).filter(AdvertsImages.advert_id == advert_id).all()
    return render_template('advert.html', title='Объявление',
                           css1=url_for('static', filename='css/style_advert.css'), advert=advert, photos=photos,
                           user=user)


@app.route('/register', methods=['GET', 'POST'])
def register():  # регистрация
    form = RegForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(Users).filter(Users.email == form.email.data).first():  # проверка логина и пароля пользователя
            return render_template('registration.html', title='Регистрация', form=form, message='такая почта уже есть')
        if db_sess.query(Users).filter(Users.login == form.login.data).first():
            return render_template('registration.html', title='Регистрация', form=form, message='такой логин уже есть')
        if form.password.data != form.password_again.data:
            return render_template('registration.html', title='Регистрация', form=form, message='пароли не совпадают')
        if request.files['file']:
            file = request.files['file']  # добавление изображения профиля в бд
            filename = secure_filename(file.filename)
            path = normpath(join(app.config['UPLOAD_FOLDER']['PROFILE_IMAGES_FOLDER'], filename))
            file.save(path)
        else:
            path = join(app.config['UPLOAD_FOLDER']['PROFILE_IMAGES_FOLDER'], 'default_image.png')
        user = Users(  # добавление пользователя
            login=form.login.data,
            email=form.email.data,
            photo=path,
            phone_number=form.phone_number.data,
            created_date=datetime.datetime.now()
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user)
        return redirect('/')
    return render_template('registration.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():  # авторизация пользователя
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


@app.errorhandler(400)  # обработчик ошибки 400
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_adverts():  # добавление объявления
    form = AdvertForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        advert = Advert(
            title=form.title.data,
            description=form.description.data,
            likes_count=0,
            city=form.city.data,
            address=form.address.data,
            created_date=datetime.datetime.now(),
            user_id=current_user.id,
            price=form.price.data,
            category_id=request.form['category'],
        )
        session.add(advert)
        session.commit()
        files = request.files.getlist('files')
        for file in files:  # добавление изображения
            filename = secure_filename(file.filename)
            path = normpath(join(app.config['UPLOAD_FOLDER']['ADVERTS_IMAGES_FOLDER'], filename))
            if not os.path.isfile(path):
                file.save(path)
            session.add(AdvertsImages(
                path=path,
                advert_id=advert.id
            ))
        session.commit()
        return redirect('/')
    return render_template('adverts_add.html', title='Объявление', form=form)


@app.errorhandler(401)
def unauthorized(_):  # обработка ошибки, если пользователь не авторизован
    return redirect('/login')


@app.route('/logout')
@login_required
def logout():  # выход из аккаунта
    logout_user()
    return redirect("/")


@app.route('/delete_advert/<advert_id>')
@login_required
def delete_advert(advert_id):  # удаление объявления
    session = db_session.create_session()
    advert = session.query(Advert).filter(Advert.id == advert_id).first()
    photos = session.query(AdvertsImages).filter(AdvertsImages.advert_id == advert_id)
    session.delete(advert)
    for i in photos:
        session.delete(i)
    session.commit()
    return redirect('/')


@app.route('/redact_advert/<advert_id>', methods=['POST', 'GET'])
def redact_advert(advert_id):  # редактирование объявления
    form = AdvertForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        advert = session.query(Advert).get(advert_id)
        advert.title = form.title.data
        advert.description = form.description.data
        advert.city = form.city.data
        advert.price = form.price.data
        advert.address = form.address.data
        session.commit()
        return redirect(f'/advert/{advert_id}')

    return render_template('adverts_add.html', title='редактирование объявления', form=form)


def main():
    db_session.global_init("db/avito_db.db")
    api.add_resource(UsersResource, '/api/users/<int:users_id>')
    api.add_resource(UsersListResources, '/api/users')
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()