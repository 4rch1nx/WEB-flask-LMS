from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField

class Algorithm_form(FlaskForm):
    run_algorithm_button = SubmitField('Запустить алгоритм')
    save_algorithm_button = SubmitField('Сохранить алгоритм')

