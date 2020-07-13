from flask import Flask

import datetime
import calendar

app = Flask(__name__)

@app.route('/')

dt1 = datetime.date.today()
dt2 = datetime.datetime.now()

def date():
  return print(dt1 ' ' dt2)

if __name__=='__main__':
  app.debug = True
  app.run()

