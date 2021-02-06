from flask import Flask, render_template, redirect
from forms import *
import pymysql
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'How long has this been going on?'

# config = {'host': "remotemysql.com",
#               'user': 'JiQRuMfhFj',
#               'password': 'J9MyW4oGCj',
#               'database': "JiQRuMfhFj"
#               }
# db = connect(**config)

connection = pymysql.connect(host='remotemysql.com',
                             user='JiQRuMfhFj',
                             password='J9MyW4oGCj',
                             database='JiQRuMfhFj',
                             cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
def main():
    return render_template('index.html', title='Главная | LateLit')


@app.route('/events')
def code():
    #show_table_query = "SELECT * FROM schedule"
    #cursor = db.cursor(True)
    #cursor.execute(show_table_query)
    #result = cursor.fetchall()

    show_table_query = "SELECT * FROM schedule"
    cursor = connection.cursor()
    cursor.execute(show_table_query)
    result = cursor.fetchall()
    for row in result:
        print(row)
    cursor.close()
    return render_template("events.html", events=result)


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


@app.route('/addEvent', methods=['GET', 'POST'])
def addEvent():
    form = AddEventForm()
    form.choices.choices = [[1, 'Понедельник'], [2, 'Вторник'], [3, 'Среда'],
                            [4, 'Четверг'], [5, 'Пятница'], [6, 'Суббота']]
    if form.validate_on_submit():
        description = form.description.data
        start_time = form.start_time.data
        end_time = form.end_time.data
        if len(form.choices.data) != 1:
            form.description.data = description
            form.start_time.data = start_time
            form.end_time.data = end_time
            return render_template('addEvent.html',
                                   title='Добавление ивента',
                                   message='Вы выбрали больше одного дня!',
                                   form=form)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM schedule")
        lastID = cursor.fetchall()[-1]['idschedule']

        cursor.execute("INSERT INTO schedule VALUES(%s, %s, %s, %s, %s, %s)",
                       (lastID + 1, lastID + 1, start_time, end_time, description, form.choices.data[0], ))
        connection.commit()
        cursor.close()
        return redirect('/events')

    return render_template('addEvent.html', title='Добавление ивента', form=form)


@app.route('/eventsByDay/<int:id>', methods=['GET', 'POST'])
def eventsByDay(id):
    days = [None, 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
    show_table_query = "SELECT * FROM schedule WHERE day=%s"
    cursor = connection.cursor()
    cursor.execute(show_table_query, (id, ))
    result = cursor.fetchall()
    for row in result:
        print(row)
    cursor.close()
    return render_template("events.html", events=result, day=days[id])


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    #app.run(port=8080, host='127.0.0.1')