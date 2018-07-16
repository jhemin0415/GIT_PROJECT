from flask import Flask, request, render_template, session


class Userinfo:
    def __init__(self, id, nickname, permission):
        self.id = id
        self.nickname = nickname
        self.permission = permission

    



app = Flask(__name__)

@app.route('/', methods = ['POST','GET'])
def main():
    if request.method == 'POST':
        return '<h1>POST SUCCESS</h1>'
        
    return render_template('main.html')

@app.route('/<name>')
def name(name):
    return '<h1>Hello %s</h1>]' %name

if __name__ == '__main__':
    app.run(host = '203.252.231.149', port = 5000, debug = True)