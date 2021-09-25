from flask import Flask
import json
app = Flask(__name__)


@app.route('/')
@app.route('/home')
def hello_world():
    return '<h1>Home</h1>'


@app.route('/user')
def user():
    return json.dumps({'name': 'alice', 'email': 'alice@outlook.com'})

if __name__ == '__main__':
    app.run()
