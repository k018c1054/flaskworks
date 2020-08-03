from flask import Flask, render_template, request
import datetime

app = Flask(__name__)

steps = []

@app.route('/')
def index():
 dt = datetime.datetime.now()
 date = dt.strftime("%m/%d %H:%M")
 step = request.form.get('step')
 if step is not None:
   steps.append((date, step))
  return render_template('kadai5-2.html', steps=steps)

if __name__=='__main__':
  app.debug = True
  app.run()