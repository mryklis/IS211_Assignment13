import sqlite3
from flask import Flask, render_template, request, redirect, session, flash


DATABASE = 'hw13.db'
SECRET_KEY = 'shhhhhhh'
USERNAME = 'admin'
PASSWORD = 'password'

conn = sqlite3.connect(DATABASE)

c = conn.cursor()

app = Flask(__name__)
app.config.from_object(__name__)

def create():
    qry = open('schema.sql').read()
    c.executescript(qry)
    c.execute('''INSERT INTO STUDENTS (ID, FIRSTNAME, LASTNAME) values (001, "John", "Smith")''')
    c.execute('''INSERT INTO QUIZZES (ID, SUBJECT, QUESTION_COUNT, QUIZ_DATE) values (001, "Python Basics", 5, "February, 5th, 2015")''')
    c.execute('''INSERT INTO RESULTS (STUDENTID, QUIZID, SCORE) values (001,001,85)''')


@app.route('/', methods=['GET'])
def index():
    return redirect('/login')


@app.route('/login',methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != USERNAME or request.form['password'] != PASSWORD:
            redirect('/login')
            error = 'Invalid Login Credentials'
        else:
            session['logged_in'] = True
            return redirect('/dashboard')

    return render_template('login.html', error=error)


@app.route('/dashboard')
def dashboard():
    if session['logged_in'] != True:
        return redirect('/login')
    else:
        c.execute('''select ID, FIRSTNAME, LASTNAME from STUDENTS''')
        students = [dict(id=row[0], first_name=row[1], last_name=row[2]) for row in c.fetchall()]
        c.execute('''select ID, SUBJECT, QUESTION_COUNT, QUIZ_DATE from QUIZZES''')
        quiz = [dict(id=row[0], subject=row[1], count=row[2], date=row[3]) for row in c.fetchall()]
        return render_template('/dashboard.html', students=students, quiz=quiz)


@app.route('/student/add', methods = ['GET','POST'])
def studentadd():
    if session['logged_in'] != True:
        return redirect('/login')
    else:
        if request.method == 'GET':
            return render_template('studentadd.html')
        elif request.method == 'POST':
            if request.form['first_name'] == '' or request.form['last_name'] == '':
                flash('empty fields not allowed')
                return redirect('/student/add')
            else:
                try:
                    f = request.form['first_name']
                    l = request.form['last_name']
                    c.execute('''insert into STUDENTS (FIRSTNAME, LASTNAME) values (?,?)''',(f,l))
                    conn.commit()
                    return redirect('/dashboard')
                except:
                    flash('error saving record')
                    return redirect('/student/add')


@app.route('/quiz/add', methods = ['GET','POST'])
def quizadd():
    if session['logged_in'] != True:
        return redirect('/login')
    else:
        if request.method == 'GET':
            return render_template('addquiz.html')
        elif request.method == 'POST':
            if request.form['subject'] == '' or request.form['count'] == '' or request.form['date'] == '':
                flash('empty fields not allowed')
                return redirect('/quiz/add')
            else:
                try:
                    sub = request.form['subject']
                    count = request.form['count']
                    d = request.form['date']
                    c.execute('''insert into QUIZZES (SUBJECT, QUESTION_COUNT, QUIZ_DATE) values (?,?,?)''',(sub, count, d))
                    conn.commit()
                    return redirect('/dashboard')
                except:
                    flash('error saving record')
                    return redirect('/quiz/add')


@app.route('/student/<id>', methods=['GET'])
def studentquiz(id):
    if session['logged_in'] != True:
        flash("You are not logged in")
        return redirect('/login')
    else:
        c.execute('select FIRSTNAME, LASTNAME from STUDENTS where ID = ?', (id))
        namelist = c.fetchall()[0]
        studentname = namelist[0] + " " + namelist[1]
        c.execute('''select QUIZID, SCORE from RESULTS where STUDENTID = ?''', (id))
        results = [dict(quiz_id=row[0], score=row[1]) for row in c.fetchall()]
        return render_template('results.html', results=results, studentname=studentname)

@app.route('/results/add', methods=['GET', 'POST'])
def addresults():
    if session['logged_in'] != True:
        flash("You are not logged in")
        return redirect('/login')
    else:
        if request.method == 'GET':
            c.execute('''select ID, SUBJECT from QUIZZES''')
            quizzes = [dict(quiz_id=row[0], subject=row[1]) for row in c.fetchall()]
            c.execute('''select ID, FIRSTNAME, LASTNAME from STUDENTS''')
            students = [dict(student_id=row[0], studentname=row[1] + " " + row[2]) for row in c.fetchall()]
            return render_template('addresult.html', quizzes=quizzes, students=students)
        elif request.method == 'POST':
            try:
                c.execute('''insert into RESULTS (STUDENTID, QUIZID, SCORE) values (?, ?, ?)''',
                             (request.form['student_id'], request.form['quiz_id'], request.form['score']))
                conn.commit()
                flash("Quiz Records Updated")
                return redirect("/dashboard")

            except:
                flash("Error Updating Record")
                return redirect("/results/add")

if __name__ == '__main__':
    create()
    app.run()
    conn.close()