from flask import Flask, render_template, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)


@app.route('/')
def index():
    photo = ["/static/img/one.PNG", "/static/img/two.PNG", "/static/img/one.PNG", "/static/img/two.PNG",
             "/static/img/one.PNG", "/static/img/two.PNG", "/static/img/one.PNG", "/static/img/two.PNG",
             "/static/img/one.PNG"]
    return render_template('chernovik.html', title='Вы тут найдете всё', photos=photo,
                           css1=url_for('static', filename='css/ww.css'))


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
