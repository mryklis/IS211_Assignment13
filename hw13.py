import sqlite3
from flask import Flask, render_template, request, redirect, session, g, url_for, abort, flash

app = Flask(__name__)

DATABASE = 'hw13.db'
DEBUG = True
SECRET_KEY = 'shhhhhhh'
USERNAME = 'admin'
PASSWORD = 'default'

conn = sqlite3.connect(DATABASE)

c = conn.cursor()

def create():

    qry = open('schema.sql').read()

    c.executescript(qry)

    c.execute('''INSERT INTO STUDENTS (ID, FIRSTNAME, LASTNAME) values (001, "John", "Smith")''')

    c.execute('''INSERT INTO QUIZZES (ID, SUBJECT, QUESTION_COUNT, QUIZ_DATE) values (001, "Python Basics", 5, "February, 5th, 2015")''')

    c.execute('''INSERT INTO RESULTS (STUDENTID, QUIZID, SCORE) values (001,001,85)''')


# @app.route('/')


# @app.route('/login')
#
#
# @app.route('/dashboard')
#
#
# @app.route('/student/add')
#
#
# @app.route('/quiz/add')
#
#
# @app.route('/results/add')


if __name__ == '__main__':
    create()
    c.execute('select * from STUDENTS, QUIZZES, RESULTS')
    print c.fetchall()
    conn.close()