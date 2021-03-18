from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, UserMixin, login_required, logout_user
from forms import *
import pymysql
import datetime

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'How long has this been going on?'
connection = pymysql.connect(host='remotemysql.com',
                             user='JiQRuMfhFj',
                             password='J9MyW4oGCj',
                             database='JiQRuMfhFj',
                             cursorclass=pymysql.cursors.DictCursor)

class User(UserMixin):
    id = 1

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.password.data == 'admin' and form.username.data == 'admin':
            user = User()
            login_user(user)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)

@login_manager.user_loader
def load_user(user_id):
    #session = db_session.create_session()
    return User()


@app.route('/logout')
@login_required
def logout():
    """ Выход """
    logout_user()
    return redirect("/")

@app.route('/')
def main():
    return render_template('index.html', title='Главная | fowtic')


@app.route('/events')
def code():
    show_table_query = "SELECT * FROM schedule"
    cursor = connection.cursor()
    cursor.execute(show_table_query)
    result = cursor.fetchall()
    #for row in result:
     #   print(row)
    cursor.close()
    return render_template("events.html", events=result, title='Список ивентов | fowtic')


@app.route('/deleteEvent/<int:id>', methods=['GET', 'POST'])
def deleteEvent(id):
    deleteQuery = f"DELETE FROM schedule WHERE idschedule=%s"
    cursor = connection.cursor()
    print(id)

    cursor.execute(deleteQuery, (id,))
    connection.commit()

    show_table_query = "SELECT * FROM schedule"
    cursor = connection.cursor()
    cursor.execute(show_table_query)
    result = cursor.fetchall()
    for row in result:
        print(row)
    cursor.close()
    return redirect('/events')


@app.route('/updateEvent/<int:id>', methods=['GET', 'POST'])
def updateEvent(id):
    form = AddEventForm()
    form.choices.choices = [[1, 'Понедельник'], [2, 'Вторник'], [3, 'Среда'],
                            [4, 'Четверг'], [5, 'Пятница'], [6, 'Суббота'], [7, 'Воскресенье']]
    arr = [[7, 'Воскресенье'], [1, 'Понедельник'], [2, 'Вторник'], [3, 'Среда'],
                            [4, 'Четверг'], [5, 'Пятница'], [6, 'Суббота']]
    st, et = 0, 0
    morning = datetime.time(8, 0, 0)  # Восемь утра
    evening = datetime.time(20, 0, 0)  # Восемь вечера
    if request.method == "GET":
        show_table_query = "SELECT * FROM schedule WHERE idschedule=%s"
        cursor = connection.cursor()
        cursor.execute(show_table_query, (id, ))
        result = cursor.fetchone()
        print('aaaaaaaaaaaaaassssssssssssssssssa')
        cursor.close()
        #print(result)
        print('привет!!!!!!!!!!!!!!')
        form.classroom.data = result['id']
        form.end_time.data = datetime.datetime.strptime(result['endTime'], '%H:%M:%S')
        form.start_time.data = datetime.datetime.strptime(result['startTime'], '%H:%M:%S')
        form.description.data = result['description']
        form.choices.data = arr[result['day']]
        form.numbOfAni.data = result['animation']
        print(type(form.start_time.data), type(morning))

    if form.validate_on_submit():
        if form.end_time.data > evening or form.end_time.data < morning or \
                form.start_time.data > evening or form.start_time.data < morning:
            return render_template('addEvent.html',
                                   title='Добавление ивента',
                                   message='Ивент может проходить только в дневное время: с 8:00 до 20:00!',
                                   form=form,
                                   action='Обновление')
        if form.start_time.data >= form.end_time.data:
            return render_template('addEvent.html',
                                   title='Добавление ивента',
                                   message='Время начала ивента меньше или равно времени конца ивента!',
                                   form=form,
                                   action='Обновление')
        if len(form.choices.data) == 0:
            return render_template('addEvent.html',
                                   title='Добавление ивента',
                                   message='Вы не выбрали день недели!',
                                   form=form,
                                   action='Обновление')
        if len(form.choices.data) > 1:
            return render_template('addEvent.html',
                                   title='Добавление ивента',
                                   message='Вы выбрали больше одного дня дня!',
                                   form=form,
                                   action='Обновление'
                                   )
        if form.numbOfAni.data < 0:
            return render_template('addEvent.html',
                                   title='Добавление ивента',
                                   message='Вы выбрали неверный номер анимации!',
                                   form=form,
                                   action='Обновление'
                                   )
        if form.classroom.data < 0:
            return render_template('addEvent.html',
                                   title='Добавление ивента',
                                   message='Номер аудитории не может быть неотрицательным числом!',
                                   form=form,
                                   action='Обновление'
                                   )
        deleteQuery = f"UPDATE schedule SET id=%s, startTime=%s, endTime=%s, " \
                      f"description=%s, day=%s, animation=%s WHERE idschedule=%s"
        cursor = connection.cursor()
        cursor.execute(deleteQuery, (form.classroom.data,
                                     str(form.start_time.data),
                                     str(form.end_time.data),
                                     form.description.data,
                                     form.choices.data[0],
                                     id,
                                     form.numbOfAni.data,
                                     ))
        connection.commit()
        cursor.close()
        print('what the fuck', form.numbOfAni.data)
        return redirect('/events')
    return render_template('addEvent.html', title='Изменение ивента | fowtic', form=form, action='Изменение')


@app.route('/addEvent', methods=['GET', 'POST'])
def addEvent():
    form = AddEventForm()
    form.choices.choices = [[1, 'Понедельник'], [2, 'Вторник'], [3, 'Среда'],
                            [4, 'Четверг'], [5, 'Пятница'], [6, 'Суббота'], [7, 'Воскресенье']]
    if form.validate_on_submit():
        description = form.description.data
        start_time = form.start_time.data
        end_time = form.end_time.data
        classroom = form.classroom.data
        number = form.numbOfAni.data
        morning = datetime.time(8, 0, 0)  # Восемь утра
        evening = datetime.time(20, 0, 0)  # Восемь вечера
        if start_time > evening or start_time < morning or end_time > evening or end_time < morning:
            return render_template('addEvent.html',
                                   title='Добавление ивента',
                                   message='Ивент может проходить только в дневное время: с 8:00 до 20:00!',
                                   form=form,
                                   action='Добавление')
        if start_time >= end_time:
            return render_template('addEvent.html',
                                   title='Добавление ивента',
                                   message='Время начала ивента меньше или равно времени конца ивента!',
                                   form=form,
                                   action='Добавление')
        if len(form.choices.data) == 0:
            return render_template('addEvent.html',
                                   title='Добавление ивента',
                                   message='Вы не выбрали день недели!',
                                   form=form,
                                   action='Добавление')
        if len(form.choices.data) > 1:
            return render_template('addEvent.html',
                                   title='Добавление ивента',
                                   message='Вы выбрали больше одного дня дня!',
                                   form=form,
                                   action='Добавление'
                                   )
        if number < 0:
            return render_template('addEvent.html',
                                   title='Добавление ивента',
                                   message='Вы выбрали неверный номер анимации!',
                                   form=form,
                                   action='Добавление'
                                   )
        if classroom < 0:
            return render_template('addEvent.html',
                                   title='Добавление ивента',
                                   message='Номер аудитории не может быть неотрицательным числом!',
                                   form=form,
                                   action='Добавление'
                                   )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM schedule")
        try:
            lastID = cursor.fetchall()[-1]['idschedule']
        except IndexError:
            lastID = 1

        cursor.execute("INSERT INTO schedule VALUES(%s, %s, %s, %s, %s, %s, %s)",
                       (lastID + 1, classroom, start_time, end_time, description, form.choices.data[0], number, ))
        connection.commit()
        cursor.close()
        print('ААААААААААААААААААААААА')
        return redirect('/events')

    return render_template('addEvent.html', title='Добавление ивента | fowtic', form=form, action='Добавление')


@app.route('/eventsByDay/<int:id>', methods=['GET', 'POST'])
def eventsByDay(id):
    days = [None, 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    # в падежных формах
    cases = [None, 'понедельник', 'вторник', 'среду', 'четверг', 'пятницу', 'субботу', 'воскресенье']
    show_table_query = "SELECT * FROM schedule WHERE day=%s"
    cursor = connection.cursor()
    cursor.execute(show_table_query, (id, ))
    result = cursor.fetchall()
    for row in result:
        print(row)
    cursor.close()
    return render_template("events.html", events=result, day=days[id], title=f'Расписание на {cases[id]} | fowtic')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    # app.run(port=8080, host='127.0.0.1')