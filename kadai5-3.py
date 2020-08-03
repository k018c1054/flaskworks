from flask import Flask, render_template, request
import datetime

app = Flask(__name__)

steps = []

def get_average(steps):
  sum = 0
  for (k,v) in steps:
    sum += v
  if len(steps) == 0:
    return 0.0
  else:
    return sum / len(steps)

@app.route('/', methods=['GET', 'POST'])
def index():
  dt = datetime.datetime.now()
  date = dt.strftime("%m/%d %H:%M")
  step = request.form.get('step')
  if step is not None:
    steps.append((date, int(step)))
  average = get_average(steps)
  return render_template('kadai5-3.html', steps = steps, average=average)

if __name__=='__main__':
  app.debug = True
  app.run()