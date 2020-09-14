from flask import Flask, render_template, request, redirect, session
import mysql.connector as db
import os, datetime, re

utododb_param = {
    'user': 'mysql',
    'host': 'localhost',
    'password': '',
    'database': 'utododb'
}

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/')
def index():
    if 'name' in session:
        li_name = str(session['name'])
        conn = db.connect(**utododb_param)
        cur = conn.cursor()
        stmt = 'SELECT * FROM list WHERE user=%s'
        cur.execute(stmt, (li_name,))
        rows = cur.fetchall()
        conn.close()
        return render_template('S-kadai3login.html', name=li_name, list=rows)
    else:
        return render_template('S-kadai3.html')

@app.route('/login', methods=['POST'])
def login():
    if request.form.get('user') and request.form.get('pw'):
        uname = request.form.get('user')
        pw = request.form.get('pw')
        conn = db.connect(**utododb_param)
        cur = conn.cursor()
        stmt = 'SELECT * FROM users WHERE id=%s'
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
    return render_template('S-kadai3new.html')

@app.route('/new_login', methods=['POST'])
def new_login():
    if request.form.get('newuser') and request.form.get('npw'):
        new_user = request.form.get('newuser')
        new_pw = request.form.get('npw')
        conn = db.connect(**utododb_param)
        cur = conn.cursor()
        stmt = 'SELECT * FROM users WHERE id=%s'
        cur.execute(stmt, (new_user,))
        rows = cur.fetchall()

        if len(rows) == 0:
            cur.execute('INSERT INTO users(id, pw) VALUES(%s, %s)',
                        (new_user, new_pw))
        else:
            for item in rows[0]:
                if new_user == item:
                    return redirect('/new')
                else:
                    cur.execute(
                        'INSERT INTO users(id, pw) VALUES(%s, %s)', (new_user, new_pw))

        conn.commit()
        cur.close()
        conn.close()
        session['name'] = new_user
        return redirect('/')

    return redirect('/new')

@app.route('/send', methods=['POST'])
def send():
    ndate = datetime.datetime.now().strftime('%y-%m-%d %H:%M')
    title = request.form.get('title')
    li_user = str(session['name'])
    if title == "":
        return redirect('/')

    conn = db.connect(**utododb_param)
    cur = conn.cursor()
    stmt = 'SELECT * FROM list WHERE user=%s'
    cur.execute(stmt, (li_user,))
    rows = cur.fetchall()
    if ',' in title or '、' in title:
        t_list = re.split('[,、]', title)
        for item in t_list:
            cur.execute('INSERT INTO todolist(date, title, user) VALUES(%s, %s, %s)',
                        (ndate, item, li_user))
    else:
        cur.execute('INSERT INTO todolist(date, title, user) VALUES(%s, %s, %s)',
                    (ndate, title, li_user))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/')

@app.route('/delete', methods=['POST'])
def delete():
    del_list = request.form.getlist('del_list')
    conn = db.connect(**utododb_param)
    cur = conn.cursor()
    for id in del_list:
        stmt = 'SELECT * FROM todolist WHERE id=%s'
        cur.execute(stmt, (id,))
        rows = cur.fetchall()
        stmt = 'DELETE FROM todolist WHERE id=%s'
        cur.execute(stmt, (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/')

if __name__ == "__main__":
    app.debug = True
    app.run()
