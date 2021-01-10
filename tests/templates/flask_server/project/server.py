from $module$.counter import ViewsCounter
from flask import Flask, render_template
app = Flask(__name__)

vc = ViewsCounter()

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html', title='$name;title$', views= vc.increment())

if __name__ == '__main__':
    app.run(port=$port$,debug=True)