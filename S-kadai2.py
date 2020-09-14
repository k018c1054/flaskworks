from flask import Flask, render_template, request, redirect, session
import mysql.connector as db
import os

db_param = {
    'user': 'mysql',
    'host': 'localhost',
    'password': '',
    'database': 'userdb'
}

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/')
def index():
    if 'name' in session:
        return render_template('S-kadai2login.html', name=str(session['name']))
    else:
        return render_template('S-kadai2.html')

@app.route('/login', methods=['POST'])
def login():
    if request.form.get('user') and request.form.get('pw'):
        uname = request.form.get('user')
        pw = request.form.get('pw')
        conn = db.connect(**db_param)
        cur = conn.cursor()
        stmt = 'SELECT * FROM list WHERE id=%s'
        cur.execute(stmt, (uname,))
        rows = cur.fetchall()

        if len(rows) == 0:
            return redirect('/')
        elif uname == rows[0][0] and pw == rows[0][1]:
            session['name'] = uname
        else:
            return redirect('/')

    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('name', None)
    return redirect('/')

@app.route('/new')
def new():
    return render_template('S-kadai2new.html')

@app.route('/new_login', methods=['POST'])
def new_login():
    if request.form.get('newuser') and request.form.get('npw'):
        new_user = request.form.get('newuser')
        new_pw = request.form.get('npw')
        conn = db.connect(**db_param)
        cur = conn.cursor()
        stmt = 'SELECT * FROM users WHERE id=%s'
        cur.execute(stmt, (new_user,))
        rows = cur.fetchall()

        if len(rows) == 0:
            cur.execute('INSERT INTO users(id, pw) VALUES(%s, %s)',(new_user, new_pw))
        else:
            for item in rows[0]:
                if new_user == item:
                    return redirect('/new')
                else:
                    cur.execute('INSERT INTO users(id, pw) VALUES(%s, %s)',(new_user, new_pw))

        conn.commit()
        cur.close()
        conn.close()
        session['name'] = new_user
        return redirect('/')

    return redirect('/new')

if __name__ == "__main__":
    app.debug = True
    app.run()
