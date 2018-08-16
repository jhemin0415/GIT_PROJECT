# -- coding: utf-8 --
from wsgiref.simple_server import make_server
from flask import Flask, render_template,\
                  session, redirect, url_for, jsonify,\
                  flash, abort, Request, request
from flask_mail import Mail, Message
from flaskext.mysql import MySQL
from random import randint
from werkzeug.routing import Rule
import base64
import codecs
import os
import datetime


app = Flask(__name__)

app.config.update(
    DEBUG = True,
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'jhemin0415@gmail.com',
	MAIL_PASSWORD = 'djdkdl8255',
    MYSQL_DATABASE_USER = 'jhemin0415',
    MYSQL_DATABASE_PASSWORD = '7dj1dk4dl4!@',
    MYSQL_DATABASE_DB = 'flask_g2g'
)
mysql = MySQL()
mysql.init_app(app)
mail = Mail(app)

app.secret_key = 'helloworld' #세션 암호화

def generate_number():
    con = mysql.connect()
    cur = con.cursor()
    cur.execute('select * from post_number_log')
    log = cur.fetchall()
    log_arr = []
    for x in log:
        log_arr.append(x[0])            
    while 1:
        filename = randint(100000000,1000000000)
        if filename in log_arr:
            pass
        else:
            cur.execute("insert into post_number_log value (%s)", (filename, ))
            con.commit()
            return filename

@app.route('/', methods = ['GET', 'POST'])
def main():

    con = mysql.connect()
    cur = con.cursor()
    cur.execute("select p.number, p.title, a.nickname, p.date, p.views, p.header, p.category \
                 from post p, account a \
                 where p.writer = a.id and p.category = '공지' \
                 order by p.date desc")
    notice_table = cur.fetchall()
    cur.execute("select p.number, p.title, a.nickname, p.date, p.views, p.header, p.category \
                 from post p, account a \
                 where p.writer = a.id and p.category != '공지' \
                 order by p.date desc")
    post_table = cur.fetchall()
    cur.execute('select * from category order by location')
    category_table = cur.fetchall()

    post_table = list(post_table)
    while len(post_table) < 10:
        post_table.append(["","","","","","","",""])
    notice_table = list(notice_table)
    while len(notice_table) < 5:
        notice_table.append(["","","","","","","",""])

    if request.method == 'POST':
        a = request.get_json()
        return jsonify(status = '0')

    return render_template('index.html', noticeData=notice_table, postData=post_table, categoryData=category_table)

@app.route('/login', methods = ['POST', 'GET'])
def login():
    con = mysql.connect()
    cur = con.cursor()
    if request.method == 'POST':
        id = request.form['loginId']
        pw = request.form['loginPW']

        cur.execute('select * from account where id = %s and pw = %s',(id, pw))
        result = cur.fetchall()
        if result:
            session['id'] = result[0][0]
            session['username'] = result[0][2]

            return redirect('/')
        else:
            return redirect('/login')
    return render_template('login.html')

@app.route('/session')
def see_session():
    return session['username']

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

@app.route('/register', methods = ['POST', 'GET'])
def register():
    con = mysql.connect()
    cur = con.cursor()
    if request.method == "POST":
        user = request.get_json()
        if user['value'] == 'id':
            cur.execute('select * from account where id = %s', (user['ID'], ))
            result = cur.fetchall()
            if result:
                return jsonify(judge = 0)
            else:
                return jsonify(judge = 1)

        if user['value'] == 'email':
            msg = Message("귀하의 회원가입을 위해 인증번호를 발송했습니다.", sender="g2G", recipients=[user['email']])
            random_code = randint(1000,10000)
            msg.html = "귀하의 인증번호는 <h1>%s</h1> 입니다." %random_code
            mail.send(msg)
            return jsonify(auth_code = random_code)

        if user['value'] == 'submit':
            cur.execute('insert into account value (%s, %s, %s, %s)', (user['ID'], user['PW'], user['UserName'], user['Email']))
            con.commit()
            return jsonify(message = 'success')

    return render_template('register.html')

@app.route('/profile', methods = ['POST', 'GET'])
def profile():
    con = mysql.connect()
    cur = con.cursor()
    profileName = request.args.get('name')
    if not profileName:
        profileName = session['username']
        cur.execute('select * from post where writer = %s order by date desc',(session['id'], ))
        result_id = cur.fetchall()
    else:
        cur.execute('select p.number, p.title, a.nickname, p.date, p.views, p.content, p.header, p.category \
                     from post p, account a \
                     where p.writer = a.id and a.nickname = %s \
                     order by date desc',(profileName, ))
        result_id = cur.fetchall()

    cur.execute('select * from category order by location')
    category = cur.fetchall()

    return render_template('profile.html', categoryData=category, post = result_id, profileName = profileName )

@app.route('/post', methods = ['POST', 'GET'])
def post():
    con = mysql.connect()
    cur = con.cursor()
    cur.execute('select * from category order by location')
    category = cur.fetchall()
    cur.execute('select * from header')
    header = cur.fetchall()
    return render_template('post_ex_3.html', category=category, header=header)

@app.route('/change_email', methods = ['POST', 'GET'])
def change_email():
    con = mysql.connect()
    cur = con.cursor()
    if request.method == "POST":
        data = request.get_json()
        if data['value'] == 'email':
            random_code = randint(1000,10000)
            msg = Message("귀하의 이메일 변경을 위해 인증번호를 발송했습니다.", sender="g2G", recipients=[data['email']])
            msg.html = "귀하의 인증번호는 <h1>%s</h1> 입니다." %random_code
            mail.send(msg)
            return jsonify(auth_code = random_code)

        if data['value'] == "auth":
            cur.execute('update account set email = %s where id = %s', (data['email'], session['id']))
            con.commit()
            return jsonify(judge = 1)

    return render_template('change_email.html')

@app.route('/change_username', methods = ['POST', 'GET'])
def change_username():
    con = mysql.connect()
    cur = con.cursor()
    if request.method =='POST':
        nickname = request.get_json()
        cur.execute('update account set nickname=%s where id = %s', (nickname['Username'], session["id"]))
        con.commit()
        return jsonify(data = 1)
    return render_template('change_username.html')

@app.route('/change_pw', methods = ['POST', 'GET'])
def change_password():
    con = mysql.connect()
    cur = con.cursor()
    if request.method =='POST':
        pw = request.get_json()
        cur.execute('select pw \
                     from account \
                     where id = %s and pw = %s', (session['id'], pw["PW"]))

        check_pw = cur.fetchone()
        if check_pw[0] == pw['PW']:
            cur.execute('update account set pw = %s where id = %s and pw = %s', (pw['new_pw'], session['id'], pw['PW']))
            con.commit()
            return jsonify(data = 1)
    return render_template('change_password.html')

@app.route('/post_list', methods = ['POST', 'GET'])
def post_list():
    con = mysql.connect()
    cur = con.cursor()
    category = request.args.get('category')
    if category:
        cur.execute('select p.number, p.title, a.nickname, p.date, p.views, p.header, p.category \
                     from post p, category c, account a \
                     where p.writer = a.id and p.category = c.name and c.E_Name = %s \
                     order by date desc',(category, ))
        result = cur.fetchall()
    else:
        cur.execute('select p.number, p.title, a.nickname, p.date, p.views, p.header, p.category \
                     from post p, account a \
                     where p.writer = a.id and category != %s \
                     order by date desc',('공지', ))
        result = cur.fetchall()
    cur.execute('select * from category order by location')
    category_result = cur.fetchall()

    return render_template('post_list.html', postList = result, category=category_result)

@app.route('/post_list/<category>', methods = ['POST', 'GET'])
def post_list_category(category):
    con = mysql.connect()
    cur = con.cursor()
    cur.execute('select * from post where category=%s' %category)
    postList = cur.fetchall()
    return render_template('post_list.html',postList = postList)

@app.route('/read_post/<int:num>', methods = ['POST', 'GET'])
def read_post(num):
    con = mysql.connect()
    cur = con.cursor()
    cur.execute('select * from post where number = %s ' %(num, ))
    post_result = cur.fetchone()

    sql = 'select distinct(number) as number, writer, contents, date \
           from post_comment \
           where upper_comment_number is null and post_num = %s and number is not null \
           order by date' %post_result[5]
    cur.execute(sql)
    comment = cur.fetchall()

    sql = 'select t0.number, t0.writer, t0.contents, t0.date \
	     , t1.number, t1.writer, t1.contents, t1.date \
           from post_comment as t0 \
           left join post_comment as t1 on t1.upper_comment_number = t0.number \
           where t0.upper_comment_number is null and t0.post_num = %s and t1.number is not null \
           order by t0.date, t1.date' %post_result[5]
    cur.execute(sql)
    comment1 = cur.fetchall()
        
    cur.execute('select count(*) from \
                 post_comment p1, post p2 \
                 where p2.number = %d and p1.post_num = p2.content' %(num))
    count = cur.fetchone()
    cur.execute('select * from category order by location')
    category = cur.fetchall()
    views = int(post_result[4])
    cur.execute('update post set views = %d where number = %d' %(views+1, num))
    con.commit()

    return render_template('read_post.html', postData = post_result, comment=comment, comment1=comment1, count = count, category=category)



@app.route('/search', methods = ['POST', 'GET'])
def search():
    con = mysql.connect()
    cur = con.cursor()
    if request.method == "POST":
        user = request.get_json()
        if user['value'] == 'search_id':
            cur.execute('select * from account where email = %s', (user['email'], ))
            result = cur.fetchone()
            if result:
                msg = Message("귀하의 아이디를 발송했습니다.", sender="g2G", recipients=[user['email']])
                msg.html = "귀하의 ID는 <h1>%s</h1> 입니다." %result[0]
                mail.send(msg)
                return jsonify(message = 1)
            else:
                return jsonify(message = 0)

        if user['value'] == 'search_pw':
            cur.execute('select * from account where email = %s and id = %s', (user['email'], user['id'] ))
            result = cur.fetchone()
            if result:
                msg = Message("귀하의 패스워드를 발송했습니다.", sender="g2G", recipients=[user['email']])
                msg.html = "귀하의 PW는 <h1>%s</h1> 입니다." %result[1]
                mail.send(msg)
                return jsonify(message = 1)
            else:
                return jsonify(message = 0)

    return render_template('search.html')

@app.route('/search_result_id', methods = ['POST', 'GET'])
def search_result_id():
    return render_template('search_result_id.html')

@app.route('/search_result_pw', methods = ['POST', 'GET'])
def search_result_pw():
    return render_template('search_result_pw.html')

@app.route('/del_post', methods = ['POST', 'GET'])
def del_post():
    con = mysql.connect()
    cur = con.cursor()
    if request.method == 'POST':
        data = request.get_json()
        if data['value'] == 'del_comment':
            
            cur.execute('delete from post_comment where number = %s', (data['comment_number']), )
            
            return jsonify(status = '1')
        else:
            cur.execute('delete from post where number = %s', (data['ID'], ))
            cur.execute('delete from post_comment where post_num = %s', (data['html']))
            cur.execute('delete from post_number_log where number = %s',(data['html']))
            os.remove('./templates/post/%s.html' %data['html'])

        con.commit()
        return jsonify(status = '1')

@app.route('/modify_comment', methods=['GET','POST'])
def modify_comment():
    con = mysql.connect()
    cur = con.cursor()
    if request.method == 'POST':
        data = request.get_json()
        cur.execute('update post_comment set contents = %s where number = %s', (data['comment'], data['comment_number']))
        con.commit()
        return jsonify(status = 1)

@app.route('/comment', methods = ['POST', 'GET'])
def comment():
    con = mysql.connect()
    cur = con.cursor()
    if request.method == 'POST':
        data = request.get_json()
        cur.execute("insert into post_comment(writer,contents,post_num,date,upper_comment_number) value(%s,%s,%s,now(),null)", (session['id'], data['comment'], data['html']))
        con.commit()
        return jsonify(status = '1')

@app.route('/recomment', methods = ['POST','GET'])
def recomment():
    con = mysql.connect()
    cur = con.cursor()
    if request.method == 'POST':
        data = request.get_json()
        cur.execute('insert into post_comment (writer,contents,post_num,date,upper_comment_number)\
                    value (%s,%s,%s,now(),%s)', (data['writer'], data['comment'], data['html'], data['upper_comment_number']))
        con.commit()
        return jsonify(status = '1')

@app.route('/modify/<int:num>', methods = ['GET','POST'])
def modify(num):
    con = mysql.connect()
    cur = con.cursor()
    cur.execute('select * from post where number = %s',(num, ))
    post = cur.fetchone()
    
    if not session or session['id'] != post[2]:
        return redirect('/')

    if request.method == 'POST':
        f = codecs.open('./templates/post/%s.html' %post[5], 'w', 'utf-8')
        contents = request.form['ir1']
        f.write(contents)
        f.close()

        return redirect('/read_post/%s' %num)

    f = codecs.open('./templates/post/%s.html' %str(post[5]), 'r', 'utf-8')
    contents = f.read()
    f.close()

    return render_template('modify_post.html', post=post, contents=contents, num=num)

###############################################
@app.route('/editor')
def editor():
    return render_template('SmartEditor2.html')

@app.route('/editor_skin')
def editor_skin():
    return render_template('SmartEditor2Skin.html')

@app.route('/editor/post', methods=['GET','POST'])
def viewer():
    con = mysql.connect()
    cur = con.cursor()
    if request.method == 'POST':
        
        a = request.form['ir1']
        print(a)
        title = request.form['postTit']
        print(title)
        category = request.form.get('category')
        header = request.form.get('header')

        if not a or not title or not category or not header:
            return '<h1>빠진 데이터가 있습니다.</h1>'

        filename = generate_number()
        print(filename)
        f = codecs.open("./templates/post/%s.html"% filename,"w",'utf-8')
        f.write(a)
        f.close()
        cur.execute("insert into post(title,writer,date ,views,content,category,header)\
                    value(%s, %s, now(), %s, %s, %s, %s)", (title, session['id'] ,0,str(filename),category,header))
        con.commit()
        return redirect('/')

@app.route('/editor_photo')
def photo():
    return render_template('photo_uploader.html')

@app.route('/editor_uploader')
def editor_uploader():
    if request.method == 'POST':
        print('posted')

    return 'asdf'

@app.route('/post/viewer/<num>')
def post_viewer(num):
    return render_template('/post/%s.html' %num)

if __name__ == '__main__':
    httpd = make_server('203.252.231.149', 80, app)
    httpd.serve_forever()

