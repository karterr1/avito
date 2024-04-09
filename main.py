from flask import Flask, redirect, request, abort, make_response, jsonify, url_for
from data import db_session
from data.user import Users
from flask import render_template
from datetime import datetime as dt
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api
from data.users_resources import UsersResource, UsersListResources

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)


@app.route('/')
def index():
    return render_template('base.html', title='Вы тут найдете всё')


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
