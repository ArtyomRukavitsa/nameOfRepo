from flask import Flask, render_template, redirect, request
from forms import *
import pymysql
import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'How long has this been going on?'
connection = pymysql.connect(host='remotemysql.com',
                             user='JiQRuMfhFj',
                             password='J9MyW4oGCj',
                             database='JiQRuMfhFj',
                             cursorclass=pymysql.cursors.DictCursor)


@app.route('/')
def main():
    return render_template('index.html', title='Главная | fowtic')


@app.route('/events')
def code():
    show_table_query = "SELECT * FROM schedule"
    cursor = connection.cursor()
    cursor.execute(show_table_query)
    result = cursor.fetchall()
    for row in result:
        print(row)
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
    if request.method == "GET":
        show_table_query = "SELECT * FROM schedule WHERE idschedule=%s"
        cursor = connection.cursor()
        cursor.execute(show_table_query, (id, ))
        result = cursor.fetchone()
        cursor.close()
        print(result)
        form.classroom.data = result['id']
        form.end_time.data = datetime.datetime.strptime(result['endTime'], '%H:%M:%S')
        form.start_time.data = datetime.datetime.strptime(result['startTime'], '%H:%M:%S')
        form.description.data = result['description']
        form.choices.data = arr[result['day']]
    if form.validate_on_submit():
        deleteQuery = f"UPDATE schedule SET id=%s, startTime=%s, endTime=%s, " \
                      f"description=%s, day=%s WHERE idschedule=%s"
        cursor = connection.cursor()
        cursor.execute(deleteQuery, (form.classroom.data,
                                     str(form.start_time.data),
                                     str(form.end_time.data),
                                     form.description.data,
                                     form.choices.data[0],
                                     id))
        connection.commit()
        cursor.close()
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
        """проверка на то, что первое время должно быть меньше второго"""
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
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM schedule")
        try:
            lastID = cursor.fetchall()[-1]['idschedule']
        except IndexError:
            lastID = 1

        cursor.execute("INSERT INTO schedule VALUES(%s, %s, %s, %s, %s, %s)",
                       (lastID + 1, classroom, start_time, end_time, description, form.choices.data[0], ))
        connection.commit()
        cursor.close()
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
    #app.run(port=8080, host='127.0.0.1')