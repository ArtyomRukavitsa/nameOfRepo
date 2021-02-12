from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TimeField, SelectMultipleField, widgets, IntegerField, PasswordField
from wtforms.validators import DataRequired, length


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class AddEventForm(FlaskForm):
    description = StringField('Описание урока', validators=[DataRequired()])
    start_time = TimeField('Время начала урока', validators=[DataRequired()])
    end_time = TimeField('Время окончания урока', validators=[DataRequired()])
    classroom = IntegerField('Аудитория', validators=[DataRequired()])
    choices = MultiCheckboxField('День недели', coerce=int)
    submit = SubmitField('Подвтердить')


class LoginForm(FlaskForm):
    username = StringField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

