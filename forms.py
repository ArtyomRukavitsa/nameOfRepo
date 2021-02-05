from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField, TimeField
from wtforms.validators import DataRequired, length


class AddEventForm(FlaskForm):
    description = StringField('Описание урока', validators=[DataRequired()])
    start_time = TimeField('Время начала урока')
    end_time = TimeField('Время окончания урока')
    submit = SubmitField('Добавить урок')