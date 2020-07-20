from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def odd():
    return render_template('kadai03-1.html', num = 10)

if __name__ == "__main__":
    app.debug = True
    app.run()
