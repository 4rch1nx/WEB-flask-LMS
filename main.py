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
from data.saved_algorithms import Saved_algorithm

from forms.authorization import RegisterForm, LoginForm, ProfileEditingForm
from forms.questions import Question_form, Answer_Question_form, Changing_question_form

#импорт констант
from constants import *

# импорт функций для работы с ESP
from esp_connection import *

# импорт функций для обработки алгоритма движения робота
from code_reader import *

app = Flask(__name__)  # объект приложения
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'  # секретный ключ для защиты от CSRF-атак

login_manager = LoginManager()  #объект менеджера авторизации пользователей
login_manager.init_app(app)


# Доделать:
# -------------------------------------------------------------------------
# 1. Постараться подсветить функции в редакторе кода во вкладке "Алгоритм"
# 2. Доделать систему сохранения алгоритма движения машинки:
#     - Сделать окно с предупреждением о том, что алгоритм не сохранён. Окно должно появляться перед выходом
#       со страницы алгоритм (информацию о сохранении / не сохранении алгоритма можно записывать в sessionStorage).
#       Также, в окне должна быть галочка "Больше не показывать"/
#
#     - Сделать систему отображения и изменения названий алгоритмов.
# 3. Сделать окно информации о сохранённом устройстве, а также о подключенном устройстве с возможностью
# отключения от него (при отсутствии подключения перенаправлять на страницу '/devices', при подлкюченном
# устройстве - на страницу с информацией о нён.
# 4. В Modal, предупреждающем о подлкючении устройства через WiFi, сделать галочку "Не показывать больше"
# 5. Дописать окна с теорией и документацией
# 6. (В конце) Сделать шаблон для ошибок (404, 400 и др.)

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
        login_user(user, remember=False)
        return redirect("/")
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
    return render_template("control.html", src_inpt="static/img/base_account_photo.jpg")


@app.route('/algorithm')
def algorithm():
    """
    Функция рендеринга страницы, на которой находится система составления алгоритма
    движений машинки
    :return: algorithm.html
    :rtype: html
    """
    code_error_message = request.args.get("code_error_message")
    saving_error_message = request.args.get("saving_error_message")
    if code_error_message is None: code_error_message = ""
    if saving_error_message is None: saving_error_message = ""
    return render_template("algorithm.html", code_error_message=code_error_message,
                           saving_error_message=saving_error_message)


@app.route('/run_algorithm')
def run_algorithm():
    code = request.args.get("algorithm")
    code_error_message = ""
    if code != "":
        functions = read_code(code)
        if type(functions) == str:
            code_error_message = functions
    return redirect(f"/algorithm?code_error_message={code_error_message}")


@app.route('/save_algorithm', methods=['GET', 'POST'])
def save_algorithm():
    code = request.args.get("algorithm")
    saving_error_message = ""
    if current_user.is_authenticated:
        if code != "":
            error = find_errors_in_code(code)
            if error is None:
                db_sess = db_session.create_session()
                saved_algorithm = Saved_algorithm(
                    algorithm=code,
                    user_id=current_user.id
                )
                db_sess.add(saved_algorithm)
                db_sess.merge(current_user)
                db_sess.commit()
                return redirect('/successful_saving')
            else:
                saving_error_message = error
        else:
            saving_error_message = "Нельзя сохранять пустой код!"
    else:
        saving_error_message = "Войдите в аккаунт / зарегистрируйтесь, чтобы сохранить ваш код!"

    return redirect(f"/algorithm?saving_error_message={saving_error_message}")


@app.route('/successful_saving')
def successful_saving():
    """
    Функция для рендеринга страницы, на которой отображается сообщение
    об успешном сохранении алгоритма движения робота
    :return: result_of_operation.html
    :rtype: html
    """
    return render_template("result_of_operation.html", page_title="Алгоритм сохранён!",
                           message="""Вы можете найти сохранённые вами алгоритмы, нажав на кнопку "Сохранённые алгоритмы"
                           на странице "Алгоритм" или в вашем профиле.
                           """,
                           other_button_message="Продолжить писать алгоритм",
                           redirection="/algorithm",
                           successful=True)

@app.route('/saved_algorithms')
def render_page_with_saved_algorithms():
    db_sess = db_session.create_session()
    algorithms = list(db_sess.query(Saved_algorithm).filter(Saved_algorithm.user_id == current_user.id))
    return render_template("saved_algorithms.html", saved_algorithms=algorithms)




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
    user_devices = []
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        user_devices = list(db_sess.query(Devices).filter(Devices.user_id == current_user.id))
    return render_template("devices.html", user_devices=user_devices)


@app.route('/searching_for_esp', methods=['GET', 'POST'])
def searching_for_esp():
    available_esp = find_ESP()
    esp_list = []
    if available_esp is not None:
        esp_list = available_esp.values()
    return render_template("searching_for_esp.html", available_esp=esp_list)


@app.route('/connect_to_esp_ssid/<ssid>')
def connect_to_esp_ssid(ssid):
    try:
        connect_to_wifi(ssid)
        return redirect(f'/successful_connection/{ssid}')
    except:
        return redirect(f'/connection_error/{ssid}')


@app.route('/successful_connection/<ssid>')
def render_successful_connection(ssid):
    return render_template("result_of_operation.html", page_title=f"Устройство {ssid} успешно подключено!",
                           message="",
                           other_button_message="Начать управлять машинкой",
                           redirection="/control",
                           successful=True)


@app.route('/connection_error/<ssid>')
def render_connection_error(ssid):
    return render_template("result_of_operation.html", page_title=f"Не удалось подключиться!",
                           message=f"Ошибка в подключении устройства {ssid}! В случае повторения ошибок задайте вопрос разработчикам!",
                           other_button_message="Попробовать снова",
                           redirection=f"/connect_to_esp_ssid/{ssid}",
                           successful=False)


@app.route('/save_device/<ssid>')
def save_device(ssid):
    db_sess = db_session.create_session()
    saved_devices = list(db_sess.query(Devices).filter(Devices.ssid == ssid))
    if not saved_devices:
        device = Devices(
            name=ssid,
            ssid=ssid
        )
        current_user.devices.append(device)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect(f"/successful_device_saving/{ssid}")
    else:
        return redirect(f"/devices")


@app.route('/successful_device_saving/<ssid>')
def render_successful_device_saving(ssid):
    return render_template("result_of_operation.html",
                           page_title=f"Устройство {ssid} сохранено!",
                           message="Вы можете найти сохраненные вами устройства на странице 'Мои устройства'. ",
                           other_button_message="Мои устройства",
                           redirection=f"/devices",
                           successful=True)


@app.route('/delete_device/<int:device_id>')
def delete_device(device_id):
    db_sess = db_session.create_session()
    device = db_sess.query(Devices).filter(Devices.id == device_id).first()
    db_sess.delete(device)
    db_sess.commit()
    return redirect('/devices')


@app.route('/questions', methods=['GET', 'POST'])
def questions():
    """
    Функция рендеринга страницы, на которой пользователи могут задать разработчикам
    свои вопросы
    :return: questions.html
    :rtype: html
    """
    form = Question_form()
    page_title = "Задайте вопрос админам WEBRobotics!"
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
        return render_template("questions.html", form=form, page_title=page_title)


@app.route('/successful_sending')
def successful_sending():
    """
    Функция для рендеринга страницы, на которой отображается сообщение
    об успешной отправке вопроса разработчикам
    :return: result_of_operation.html
    :rtype: html
    """
    return render_template("result_of_operation.html", page_title="Вопрос отправлен!",
                           message="Спасибо за отправку вопроса! Админ ответит Вам в ближайшее время!",
                           other_button_message="Задать еще вопрос",
                           redirection="/questions",
                           successful=True)


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


@app.route("/сhanging_question/<int:id>", methods=['GET', 'POST'])
def change_question(id):
    page_title = "Изменение вопроса"

    form = Changing_question_form()
    if request.method == "GET":
        db_sess = db_session.create_session()
        question = db_sess.query(Question).filter(Question.id == id, Question.user_id == current_user.id).first()

        form.theme.data = question.theme
        form.question.data = question.question
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        question = db_sess.query(Question).filter(Question.id == id, Question.user_id == current_user.id).first()
        question.theme = form.theme.data
        question.question = form.question.data
        db_sess.commit()
        return redirect("/account")
    return render_template("questions.html", form=form, page_title=page_title)


@app.route("/delete_question/<int:id>", methods=['GET', 'POST'])
def delete_question(id):
    db_sess = db_session.create_session()
    question = db_sess.query(Question).filter(Question.id == id).first()
    db_sess.delete(question)
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
