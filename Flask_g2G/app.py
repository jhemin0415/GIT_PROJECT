from flask import Flask, request, render_template, session
from flask_socketio import SocketIO, emit, join_room

class Userinfo:
    def __init__(self, id, nickname, permission):
        self.id = id
        self.nickname = nickname
        self.permission = permission

    



app = Flask(__name__)

@app.route('/', methods = ['POST','GET'])
def main():
    if request.method == 'POST':
        name = request.form['name']
        return '<h1>Hello %s</h1>' %name
        
    return render_template('main.html')

@app.route('/<name>')
def hello_name(name):
    name = name + 1
    return '<h1>HELLO %s</h1>' %name


if __name__ == '__main__':
    app.run(host = '203.252.231.40', port = 5000, debug = True)

    print("1")