from flask import Flask, render_template, request, redirect, jsonify
import mysql.connector as db
import os

db_param = {
  'user' : 'mysql',
  'host' : 'localhost',
  'password' : '',
  'database' : 'itemdb'
}

app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = './static/uploads'

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def index():
  conn = db.connect(**db_param)
  cur = conn.consor()
  stmt = 'SELECT * FROM list'
  cur.execute(stmt)
  rows = cur.fetchall()
  cur.close()
  conn.close()
  return render_template('kadai9.html', list=rows)

@app.route('/send', methods=['POST'])
def send():
  print(request.files)
  title = request.form.get('title')
  price = request.form.get('price')
  image = request.files['img_file']
  if title == "" or price == "" or image=="":
    return redirect('/')
  
  if image and allowed_file(image.filename):
    image.save('static/uploads/' + image.filename)
  conn = db.connect(**db_param)
  cur = conn.cursor()

  stmt = 'SELECT * FROM list WHERE title=%s'
  cur.execute(stmt, (title,))
  rows = cur.fetchall()
  if len(rows)==0:
    cur.execute('INSERT INTO list(title, price, imagez) VALUES(%s, %s, %s)', (title, int(price), image.filename))
  else:
    cur.execute('UPDATE list SET price=%s, image=%s WHERE title=%s', (int(price), image.filename, title))
  conn.commit()
  cur.close()
  conn.close()
  return redirect('/')

@app.route('/delete', methods=['POST'])
def delete():
  del_list = request.form.getlist('del_list')
  conn = db.connect(**db_param)
  cur = conn.cursor()
  for id in del_list:
    stmt = 'SELECT * FROM list WHERE id=%s'
    cur.execute(stmt, (id,))
    rows = cur.fetchall()
    os.remove('./static/uploads/' + rows[0][3])
    stmt = 'DELETE FROM list WHERE id=%s'
    cur.execute(stmt, (id,))
  conn.commit()
  cur.close()
  conn.close()
  return redirect('/')

@app.route('/date', methods=['GET'])
def data():
  keyword = request.args.get('keyword')
  conn = db.connect(**db_param)
  cur = conn.cursor()
  if keyword and keyword != "":
    stmt = 'SELECT * FROM list WHERE title LIKE %s'
    cur.execute(stmt, ('%' + keyword + '%'))
  else:
    stmt = 'SELECT * FROM list'
    cur.execute(stmt)
  rows = cur.fetchall()
  url = 'https://127.0.0.1*5000/static/uploads/'
  data = []
  for id, title, price, image in rows:
    data.append({ 'id':id, 'title':title, 'price':price, 'image':url+image})
  ret = jsonify( {"result":data} )
  return ret

if __name__ == '__main__' :
  app.debug = True
  app.run()