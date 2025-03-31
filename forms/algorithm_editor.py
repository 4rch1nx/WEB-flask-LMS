from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField

class Algorithm_form(FlaskForm):
    go_ahead_button = SubmitField("Вперёд")
    go_back_button = SubmitField("Назад")
    turn_left_button = SubmitField("Налево")
    turn_right_button = SubmitField("Направо")
    code_field = TextAreaField("Алгоритм:")
    run_algorithm_button = SubmitField('Отправить')
    save_algorithm_button = SubmitField('Сохранить алгоритм')

