
import re  
import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from datetime import datetime, timedelta
import MySQLdb.cursors

app = Flask(__name__) 

app.secret_key = 'abcdefgh'
  
app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'cs353hw4db'
  
mysql = MySQL(app)  

@app.route('/')

@app.route('/login', methods =['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM User WHERE username = % s AND password = % s', (username, password,))
        user = cursor.fetchone()
        if user:              
            session['loggedin'] = True
            session['userid'] = user['id']
            session['username'] = user['username']
            session['email'] = user['email']
            message = 'Logged in successfully!'
            return redirect(url_for('tasks'))
        else:
            message = 'Please enter correct email / password !'
    return render_template('login.html', message = message)


@app.route('/register', methods =['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM User WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            message = 'Choose a different username!'
  
        elif not username or not password or not email:
            message = 'Please fill out the form!'

        else:
            cursor.execute('INSERT INTO User (id, username, email, password) VALUES (NULL, % s, % s, % s)', (username, email, password,))
            mysql.connection.commit()
            message = 'User successfully created!'

    elif request.method == 'POST':

        message = 'Please fill all the fields!'
    return render_template('register.html', message = message)

@app.route('/tasks', methods =['GET', 'POST'])
def tasks():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM Task WHERE user_id = %s ORDER BY deadline;', (session['userid'],))
     tasks = cursor.fetchall()
    
     cursor.execute("SELECT * FROM Task WHERE user_id = %s AND status = 'Done' ORDER BY done_time;", (session['userid'],))
     completed = cursor.fetchall()
     cursor.execute('SELECT * FROM TaskType;')
     types = cursor.fetchall()
     return render_template('tasks.html', tasks=tasks, completed=completed, session=session, types = types)

@app.route('/analysis', methods =['GET', 'POST'])
def analysis():
    return "Analysis page"

@app.route('/add_task', methods =['POST'])
def add_task():
    session['message'] = ''
    message = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if not session['loggedin']:
        message = 'You are not logged in to the system!'
    else:
        if request.method == 'POST' and 'task_type' in request.form:
            cursor.execute('SELECT * FROM TaskType WHERE type = % s', (request.form['task_type'], ))
            type = cursor.fetchone()
            if not type:
                message = 'Task type is not valid!'
        if request.form['title'] == '':
            message = 'Title cannot be empty!'
        elif request.form['deadline_date'] == '':
            message = 'Deadline date cannot be empty!'
        elif request.form['deadline_time'] == '':
            message = 'Deadline time cannot be empty!'
        elif request.method == 'POST' and 'title' in request.form and 'description' in request.form and 'deadline_time' in request.form and 'deadline_date' in request.form and 'task_type' in request.form:
            now = datetime.now()
            adjusted_time = now + timedelta(hours=3)
            current_time = adjusted_time.strftime("%Y-%m-%d %H:%M:%S")
            deadline = request.form['deadline_date'] + ' ' + request.form['deadline_time']

            if deadline < current_time:
                message = 'Deadline cannot be before current time!'
            else:
                cursor.execute('''
                INSERT INTO Task(
                    title,
                    description,
                    status,
                    deadline,
                    creation_time,
                    done_time,
                    user_id,  
                    task_type
                ) VALUES(
                    %s,
                    %s,
                    'Todo',
                    %s,
                    %s,
                    NULL,
                    %s,
                    %s
                );
                ''', (request.form['title'],request.form['description'],deadline,current_time,session['userid'],request.form['task_type'],))

                mysql.connection.commit()
                message = 'Your task is successfully created!'
        else:
            message = 'Please check the task information!'
        
        session['message'] = message
    return redirect(url_for('tasks'))

@app.route('/update', methods =['POST'])
def update():
    message = ''
    session['message'] = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    if session['loggedin'] and 'title' in request.form and 'description' in request.form and 'task_type' in request.form and 'deadline_time' in request.form and 'deadline_date' in request.form:
        if request.form['title'] == '':
            message = 'Title cannot be empty!'
        elif request.form['deadline_date'] == '':
            message = 'Deadline date cannot be empty!'
        elif request.form['deadline_time'] == '':
            message = 'Deadline time cannot be empty!'
        else:
            cursor.execute('UPDATE Task SET title=%s WHERE id=%s;', (request.form['title'], session['selected']['id'],))
            cursor.execute('UPDATE Task SET description = %s WHERE id = %s;', (request.form['description'],session['selected']['id'],))
            cursor.execute('UPDATE Task SET task_type = %s WHERE id = %s;', (request.form['task_type'],session['selected']['id'],))
            deadline = request.form['deadline_date'] + ' ' + request.form['deadline_time']
            cursor.execute('UPDATE Task SET deadline = %s WHERE id = %s;', (deadline,session['selected']['id'],))
            mysql.connection.commit()
            session['selected'] = None
            message = "Task updated successfully!"
    session['message'] = message
    
    return redirect(url_for('tasks'))

@app.route('/select/<int:id>', methods =['GET'])
def select(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    cursor.execute('SELECT * FROM Task WHERE id = %s;', (id,))
    task = cursor.fetchone()
    
    session['selected'] = task
    
    return redirect(url_for('tasks'))

@app.route('/cancel', methods =['GET'])
def cancel():
    session['selected'] = None
    
    return redirect(url_for('tasks'))


@app.route('/logout', methods =['GET'])
def logout():
    session['loggedin'] = False
    session['userid'] = ""
    session['username'] = ""
    session['email'] = ""
    session['selected'] = None
    session['message'] = ''
    
    return redirect(url_for('login'))

@app.route('/delete/<int:id>', methods =['GET'])
def delete(id):
    session['message'] = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if session['loggedin']:
        cursor.execute('DELETE FROM Task WHERE id = %s;', (id,))
        mysql.connection.commit()
    return redirect(url_for('tasks'))

@app.route('/uncomplete/<int:id>', methods =['GET'])
def uncomplete(id):
    session['message'] = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if session['loggedin']:
        cursor.execute('UPDATE Task SET status="Todo", done_time=NULL WHERE id = %s;', (id,))
        mysql.connection.commit()
    return redirect(url_for('tasks'))

@app.route('/complete/<int:id>', methods =['GET'])
def complete(id):
    session['messsage'] = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    now = datetime.now()
    adjusted_time = now + timedelta(hours=3)
    current_time = adjusted_time.strftime("%Y-%m-%d %H:%M:%S")
    if session['loggedin']:
        cursor.execute('UPDATE Task SET status= "Done", done_time=%s WHERE id = %s;', (current_time, id,))
        mysql.connection.commit()
    return redirect(url_for('tasks'))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
