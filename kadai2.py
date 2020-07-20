from flask import Flask
import datetime

app = Flask(__name__)

@app.route('/')

def date():
  dt = datetime.datetime.now()
  return dt.strftime('%m-%d %H:%M')

if __name__=='__main__':
  app.debug = True
  app.run()

