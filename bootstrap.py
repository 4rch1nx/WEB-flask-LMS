import requests
from flask import Flask, render_template, redirect
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
ESP_IP = "http://192.168.4.1"  # ESP8266 AP mode IP

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Имя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

def get_description():
    with open("description.txt", 'r', encoding="utf-8") as description_file:
        description = description_file.readlines()
        for i in description:
            i = i.strip()
        return description

@app.route('/')
@app.route('/index')
@app.route('/main')
def index():
    description = get_description()
    return render_template("main.html", description=description)


@app.route('/control')
def control():
    return render_template("control.html")

@app.route("/control/toggle_led")
def toggle_led():
    try:
        response = requests.get(f"{ESP_IP}/toggle")
        return response.text
    except requests.exceptions.RequestException:
        return "Error: ESP not reachable"

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

@app.route('/personalisation', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('personalisation.html', form=form)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')