from flask import Flask, render_template
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
  cur = conn.consor()
  stmt = 'SELECT * FROM books'
  cur.execute(stmt)
  rows = cur.fetchall()
  cur.close()
  conn.close()
  return render_template('kadai7.html', books=rows)

if __name__ == '__main__' :
  app.debug = True
  app.run()