from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret123'


@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        student_id = request.form['studentId']
        password = request.form['password']
        
        conn = sqlite3.connect('student.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE id=? AND password=?", (student_id, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['id'] = user[0]      # ID
            session['name'] = user[1]    # Name
            session['email'] = user[2]   # Email
            return redirect('/student')
        else:
            return "Invalid login!"
    return render_template('login.html')


@app.route('/student')
def student():
    if 'name' in session and 'email' in session and 'id' in session:
        return render_template('student.html',
                               name=session['name'],
                               email=session['email'],
                               student_id=session['id'])
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)