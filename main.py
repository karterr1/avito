from flask import Flask, redirect, request, abort, make_response, jsonify, url_for
from data import db_session
from data.users import User
from flask import render_template
from datetime import datetime as dt
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/index')
def index():
    return "Привет, Яндекс!"


def main():
    db_session.global_init("db/avito_db.db")


if __name__ == '__main__':
    main()
    app.run(port=8080, host='127.0.0.1')
