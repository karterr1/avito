from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/')
def index():
    photo = ["/static/img/one.PNG", "/static/img/two.PNG", "/static/img/one.PNG", "/static/img/two.PNG",
             "/static/img/one.PNG", "/static/img/two.PNG", "/static/img/one.PNG", "/static/img/two.PNG",
             "/static/img/one.PNG"]
    return render_template('index.html', title='Вы тут найдете всё', photos=photo,
                           css1=url_for('static', filename='css/style.css'))


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
