from flask import Flask, render_template

app = Flask(__name__)

data = []

@app.route('/user/<username>/')
def name(username):
    data.append(username)
    return render_template('kadai04.html', message=username)

@app.route('/list/')
def a_list():
    return render_template('list.html', list=data)

if __name__ == "__main__":
    app.debug = True
    app.run()
