from flask import flask, request, render_template, session
from flask_socketio import SocketIO, emit, join_room

class Userinfo:
    def __init__(self, )



app = Flask(__name__)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/login', methods = ['GET','POST'])
def post_login():
    if request.method == 'POST':
        session['userinfo'] = 

if __name__ == '__main__':
    app.run(host = '203.252.231.149', port = 5000, debug = True)