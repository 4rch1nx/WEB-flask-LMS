import requests
from flask import Flask
from flask import render_template, redirect, session, make_response, request, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user


from data.users import User
from data.devices import Devices
from data import db_session
from forms.authorization import RegisterForm, LoginForm

from constants import *


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form, message="")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form, message="")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

def get_description():
    """
    Функция, читающая описание проекта из файла.
    Нужна для последующего размещения описания на главной странице
    :return: description
    :rtype: list
    Возвращает описание в виде списка строк
    """
    with open("description.txt", 'r', encoding="utf-8") as description_file:
        description = description_file.readlines()
        for i in description:
            i = i.strip()
        return description

@app.route('/')
@app.route('/main')
def main():
    """
    Функция рендеринга главной страницы
    :return:
    """
    description = get_description()
    return render_template("main.html", description=description)

@app.route("/toggle_led")
def toggle_led():
    try:
        response = requests.get(f"{ESP_IP}/toggle", timeout=2)
        return response.text
    except requests.exceptions.RequestException:
        return "Error"

@app.route("/check_status")
def check_status():
    try:
        response = requests.get(f"{ESP_IP}/status", timeout=2)
        if response.text == "CONNECTED":
            return "ESP8266 is Online"
    except requests.exceptions.RequestException:
        return "ESP8266 is Offline"

@app.route('/control')
def control():
    return render_template("control.html")

@app.route('/algorithm')
def algorithm():
    return render_template("algorithm.html")

@app.route('/theory')
def theory():
    return render_template("theory.html")

@app.route('/documentation')
def documentation():
    return render_template("documentation.html")

@app.route('/devices')
def devices():
    return render_template("devices.html")

@app.route('/questions')
def questions():
    return render_template("questions.html")

@app.route('/about')
def about():
    return render_template("about.html")

# @app.route('/personalisation', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         return redirect('/success')
#     return render_template('personalisation.html', form=form)


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    app.run(debug=True, port=8080, host='0.0.0.0')