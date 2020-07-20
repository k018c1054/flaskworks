from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def subject():
    l_sub = {"英語":87, "数学":90, "国語":45, "理科":76, "社会":31}
    return render_template('kadai03-2.html', sub = l_sub)

if __name__ == "__main__":
    app.debug = True
    app.run()
