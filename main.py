from flask import Flask, render_template, redirect
from mysql.connector import connect, Error
from forms import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'How long has this been going on?'

config = {'host': "remotemysql.com",
              'user': 'JiQRuMfhFj',
              'password': 'J9MyW4oGCj',
              'database': "JiQRuMfhFj"
              }
db = connect(**config)

@app.route('/')
def main():
    return render_template('index.html', title='Главная | LateLit')


@app.route('/events')
def code():
    show_table_query = "SELECT * FROM schedule"
    cursor = db.cursor(True)
    cursor.execute(show_table_query)
    result = cursor.fetchall()
    for row in result:
        print(row)
    return render_template("events.html", events=result)


@app.route('/deleteEvent/<int:id>', methods=['GET', 'POST'])
def deleteEvent(id):
    deleteQuery = f"DELETE FROM schedule WHERE idschedule=%s"
    cursor = db.cursor()
    print(id)

    cursor.execute(deleteQuery, (id,))
    db.commit()

    show_table_query = "SELECT * FROM schedule"
    cursor = db.cursor(True)
    cursor.execute(show_table_query)
    result = cursor.fetchall()
    for row in result:
        print(row)
    return redirect('/events')


@app.route('/addEvent', methods=['GET', 'POST'])
def addEvent():
    form = AddEventForm()
    if form.validate_on_submit():
        description = form.description.data
        start_time = form.start_time.data
        end_time = form.end_time.data


        cursor = db.cursor(True)
        cursor.execute("SELECT * FROM schedule")
        lastID = cursor.fetchall()[-1][0]

        cursor.execute("INSERT INTO schedule VALUES(%s, %s, %s, %s, %s)",
                       (lastID + 1, lastID + 1, start_time, end_time, description, ))
        db.commit()
        return redirect('/events')

    return render_template('addEvent.html', title='Добавление ивента', form=form)





if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')