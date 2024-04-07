from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('base.html', title='Вы тут найдете всё')


@app.route('/register', methods=['GET', 'POST'])
def register():
    pass


@app.route('/login', methods=['GET', 'POST'])
def login():
    pass


def main():
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
