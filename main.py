# импорт необходимых модулей
import requests
from flask import Flask
from flask import render_template, redirect, session, make_response, request, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

#импорт классов из других файлов
from data.users import User
from data.devices import Devices
from data import db_session
from data.questions import Question

from forms.authorization import RegisterForm, LoginForm
from forms.questions import Question_form


#импорт констант
from constants import *


app = Flask(__name__) # объект приложения
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key' # секретный ключ для защиты от CSRF-атак

login_manager = LoginManager() #объект менеджера авторизации пользователей
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    """
    Функция для получения пользователя из базы данных по ID
    :param user_id: ID пользователя в базе данных
    :type: int
    :return: Даннные пользователя из базы данных
    """
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Функция рендеринга окна регистрации, отвечающая за регистрацию пользователей в приложении
    и добавления пользователей в базу данных
    :return: register.html
    :rtype: html
    html-страница регистрации
    """
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
    """
    Функция рендеринга окна входа в аккаунт в приложении. Отвечает за проверку логина
    и пароля и авторизацию пользователя.
    :return: login.html
    :rtype: html
    html-страница авторизации
    """
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
    """
    Функция выхода из аккаунта в приложении
    :return: main.html
    :rtype: html
    Функция перенаправляет пользователя на главную страницу, предварительно
    выйдя из аккаунта
    """
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
    :return: main.html
    :rtype: html
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
    """
    Функция рендеринга страницы, на которой находится система управления машинкой
    :return: control.html
    :rtype: html
    """
    return render_template("control.html")

@app.route('/algorithm')
def algorithm():
    """
    Функция рендеринга страницы, на которой находится система составления алгоритма
    движений машинки
    :return: algorithm.html
    :rtype: html
    """
    return render_template("algorithm.html")

@app.route('/theory')
def theory():
    """
    Функция рендеринга страницы, на которой находится теория по некотоым аспект
    робототехники
    :return: theory.html
    :rtype: html
    """
    return render_template("theory.html")

@app.route('/documentation')
def documentation():
    """
    Функция рендеринга страницы, на которой находится документация приложения
    и некоторая общая информация о проекте
    :return: documentation.html
    :rtype: html
    """
    return render_template("documentation.html")

@app.route('/devices')
def devices():
    """
    Функция рендеринга страницы, на которой находится информация об устройствах
    конкретного пользователя
    :return: devices.html
    :rtype: html
    """
    return render_template("devices.html")

@app.route('/questions', methods=['GET', 'POST'])
def questions():
    """
    Функция рендеринга страницы, на которой пользователи могут задать разработчикам
    свои вопросы
    :return: questions.html
    :rtype: html
    """
    form = Question_form()
    if request.method == "POST":
        db_sess = db_session.create_session()
        question = Question(
            theme=form.theme.data,
            question=form.question.data
        )
        current_user.questions.append(question)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect("/successful_sending")
    else:
        return render_template("questions.html", form=form)

@app.route('/successful_sending')
def successful_sending():
    """
    Функция для рендеринга страницы, на которой отображается сообщение
    об успешной отправке вопроса разработчика
    :return: successful_operation.html
    :rtype: html
    """
    return render_template("successful_operation.html", page_title="Вопрос отправлен!",
                           message="Спасибо за отправку вопроса! Админ ответит Вам в ближайшее время!",
                           other_button_message="Задать еще вопрос",
                           redirection="/questions")


@app.route('/about')
def about():
    """
    Функция рендеринга страницы, на которой находится информация о разработчиках
    приложения
    :return: devices.html
    :rtype: html
    """
    return render_template("about.html")


if __name__ == '__main__':
    db_session.global_init("db/blogs.db") #инициализация базы данных
    app.run(debug=True, port=8080, host='0.0.0.0') #запуск сервера