# импорт необходимых модулей
import requests
import base64
from flask import Flask
from flask import render_template, redirect, session, make_response, request, abort, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

#импорт классов из других файлов
from data.users import User
from data.devices import Devices
from data import db_session
from data.questions import Question, Answer

from forms.authorization import RegisterForm, LoginForm, ProfileEditingForm
from forms.questions import Question_form, Answer_Question_form

#импорт констант
from constants import *

# импорт функций для работы с ESP
from esp_connection import *

app = Flask(__name__)  # объект приложения
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'  # секретный ключ для защиты от CSRF-атак

login_manager = LoginManager()  #объект менеджера авторизации пользователей
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


@app.route('/control', methods=['GET', 'POST'])
def control():
    """
    Функция рендеринга страницы, на которой находится система управления машинкой
    :return: control.html
    :rtype: html
    """
    if request.method == 'GET':
        return render_template("control.html", src_inpt="static/img/base_account_photo.jpg")
    elif request.method == 'POST':
        f = request.files['file']
        img = str(base64.b64encode(bytes(f.read())))
        img = img[2:-2]
        return render_template("control.html", src_inpt=f"data:image/jpeg;base64, {img}")


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
    :return: toggle.html
    :rtype: html
    """
    db_sess = db_session.create_session()
    db_sess.query()
    user_devices = list(db_sess.query(Devices).filter(Devices.id == current_user.id))
    return render_template("devices.html", user_devices=user_devices)

@app.route('/searching_for_esp', methods=['GET', 'POST'])
def searching_for_esp():
    available_esp = find_ESP()
    esp_list = []
    if available_esp is not None:
        esp_list = available_esp
    return render_template("searching_for_esp.html", available_esp=esp_list)


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
    :return: toggle.html
    :rtype: html
    """
    return render_template("about.html")


@app.route('/account', methods=['GET', 'POST'])
def account():
    form = ProfileEditingForm()

    db_sess = db_session.create_session()
    questions = []
    answers = []
    if request.method == "GET":
        users = db_sess.query(User).filter(User.id == current_user.id).first()
        if users:
            form.name.data = users.name
            form.email.data = users.email
            form.password.data = ''
        db_answer = db_sess.query(Question).filter(Question.user_id == users.id)
        for q in db_answer:
            questions.append(q)
        for i in questions:
            answer = db_sess.query(Answer).filter(Answer.question_id == i.id).first()
            if answer is not None:
                answers.append(answer)

    if request.method == "POST" and form.validate_on_submit():
        users = db_sess.query(User).filter(User.id == current_user.id).first()
        if users:
            users.name = form.name.data
            users.email = form.email.data
            if form.password.data:
                users.set_password(form.password.data)
            db_sess.commit()
            return redirect("/main")
        else:
            abort(404)
    if request.method == "POST" and not form.validate_on_submit():
        file = request.files['profile_photo']
        photo = str(base64.b64encode(bytes(file.read())))
        if len(photo) > 3:
            photo = photo[2:-2]
            user = db_sess.query(User).filter(User.id == current_user.id).first()
            user.src_avatar = f"data:image/jpeg;base64, {photo}"
            db_sess.commit()
        return redirect("/account")

    return render_template('account.html', form=form, questions=questions,
                           answers=answers, message="", input_src=current_user.src_avatar)

@app.route("/delete_photo")
def delete_photo():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    user.src_avatar = DEFAULT_PROFILE_PHOTO
    db_sess.commit()
    return redirect("/account")

@app.route('/admin_account')
def admin_account():
    db_sess = db_session.create_session()
    all_questions = db_sess.query(Question)
    questions = []
    for q in all_questions:
        if q is not None:
            if not q.is_answered:
                questions.append(q)
    return render_template("admin_account.html", questions=questions)


@app.route('/answer_question/<int:id>', methods=['GET', 'POST'])
def answer_question(id):
    form = Answer_Question_form()
    db_sess = db_session.create_session()
    question = db_sess.query(Question).filter(Question.id == id).first()
    if form.validate_on_submit():
        answer = Answer(
            question_theme=question.theme,
            question=question.question,
            answer=form.answer.data,
            question_id=id
        )
        question.is_answered = True
        db_sess.add(answer)
        db_sess.commit()
        return redirect('/admin_account')
    else:
        #print(form)
        return render_template('answer_the_question_form.html', form=form, question=question.question)


if __name__ == '__main__':
    db_session.global_init("db/main.db")  #инициализация базы данных
    app.run(debug=True, port=8080, host='0.0.0.0')  #запуск сервера
