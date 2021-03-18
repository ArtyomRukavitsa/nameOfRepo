from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TimeField, SelectMultipleField, widgets, IntegerField, PasswordField
from wtforms.validators import DataRequired, length


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class AddEventForm(FlaskForm):
    description = StringField('Описание урока', validators=[DataRequired()])
    start_time = TimeField('Время начала урока. Пример: 12:00', validators=[DataRequired()])
    end_time = TimeField('Время окончания урока. Пример: 13:00', validators=[DataRequired()])
    classroom = IntegerField('Аудитория', validators=[DataRequired()])
    numbOfAni = IntegerField('Номер анимации<br/>'
                             '1. Алгебра\t'
                             '2. Английский язык\t'
                             '3. Биология\t'
                             '4. География\t'
                             '5. Геометрия\t'
                             '6. История\t'
                             '7. Информатика\t'
                             '8. Литература\n'
                             '9. ОБЖ\n'
                             '10. Обществознание\n'
                             '11. Русский язык\n'
                             '12. Физика\n'
                             '13. Физкультура\n'
                             '14. Химия', validators=[DataRequired()])
    choices = MultiCheckboxField('День недели', coerce=int)
    submit = SubmitField('Подтвердить')


class LoginForm(FlaskForm):
    username = StringField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

