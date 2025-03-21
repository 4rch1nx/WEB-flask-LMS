from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class Question_form(FlaskForm):
    theme = TextAreaField("Тема:", validators=[DataRequired()])
    question = TextAreaField("Ваш вопрос:", validators=[DataRequired()])
    submit = SubmitField('Отправить')

class Answer_Question_form(FlaskForm):
    answer = TextAreaField("Ответ на вопрос:", validators=[DataRequired()])
    submit = SubmitField('Отправить')

