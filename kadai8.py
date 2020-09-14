from flask import Flask, render_template, request, redirect
import mysql.connector as db

db_param = {
  'user' : 'mysql',
  'host' : 'localhost',
  'password' : '',
  'database' : 'db1'
}

app = Flask(__name__)

@app.route('/')
def index():
  conn = db.connect(**db_param)
  cur = conn.cursor()
  stmt = 'SELECT * FROM books'
  cur.execute(stmt)
  rows = cur.fetchall()
  cur.close()
  conn.close()
  return render_template('kadai8.html', books=rows)

@app.route('/send', methods=['POST'])
def send():
  title = request.form.get('title')
  price = request.form.get('price')
  if title== "" or price== "":
    return redirect('/')
  conn = db.connect(**db_param)
  cur = conn.cursor()

  stmt = ' SELECT * FROM books WHERE title=%s '
  cur.execute(stmt, (title,))
  rows = cur.fetchall()
  if len(rows)==0:
    cur.execute('INSERT INTO books(title, price) VALUES(%s, %s)', (title, int(price)))
  else:
    cur.execute('UPDATE books SET price=%s WHERE title=%s', (int(price), title))
  conn.commit()
  cur.close()
  conn.close()
  return redirect('/')

@app.route('/delete', methods=['POST'])
def delete():
  del_list = request.form.getlist('del_list')
  conn = db.connect(**db_param)
  cur = conn.cursor()
  stmt = 'DELETE FROM books WHERE id=%s'
  for id in del_list:
    cur.execute(stmt, (id,))
  conn.commit()
  cur.close()
  conn.close()
  return redirect('/')

if __name__ == '__main__' :
  app.debug = True
  app.run()