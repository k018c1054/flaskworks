from flask import Flask, render_template, request, session, redirect
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/')
def index():
  if 'username' in session:
    return render_template('kadai7.html', username=str(session['username']))
  else:
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
  if request.form.get('username'):
    session['username'] = request.form.get('username')
  return redirect('/')

@app.route('/logout')
def logout():
  session.pop('username', None)
  return render_template('login.html')

if __name__=='__main__':
  app.debug = True
  app.run()