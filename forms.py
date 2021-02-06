from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TimeField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, length



class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class AddEventForm(FlaskForm):
    description = StringField('Описание урока', validators=[DataRequired()])
    start_time = TimeField('Время начала урока')
    end_time = TimeField('Время окончания урока')
    choices = MultiCheckboxField('Routes', coerce=int)
    submit = SubmitField('Добавить урок')

