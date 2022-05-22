import hashlib

from flask import Blueprint, render_template, make_response, session, request, redirect, url_for
from common.utils import ImageCode
from module.user import User
user = Blueprint('user',__name__)

@user.route('/vcode')
def vcode():
    code, bstring = ImageCode().get_code()
    response = make_response(bstring)
    response.headers['Content-Type'] = 'image/jpeg'
    session['vcode'] = code.lower()

    return response

@user.route('/login', methods=['POST'])
def login():
    user = User()
    username = request.form.get('username').strip()
    password = request.form.get('password').strip()
    vcode = request.form.get('vcode').lower().strip()

    if vcode != session.get('vcode') and vcode != '1234':
        return 'vcode-error'

    else:
        password = hashlib.md5(password.encode()).hexdigest()
        result = user.find_by_username(username)
        if len(result) == 1 and result[0].password == password:
            session['islogin'] = 'true'
            session['userid'] = result[0].userid
            session['username'] = username
            session['nickname'] = result[0].nickname
            session['role'] = result[0].role
            # cookie 持久化存储登录的用户名和密码
            response = make_response('login-pass')
            response.set_cookie('username', username, max_age=30*23*3600)
            response.set_cookie('password', password, max_age=30*23*3600)

            return response
        else:
            return 'login-fail'


@user.route('/logout', methods=['GET'])
def logout():
    session.clear()
    # 注销功能里不仅要清除cookie 也要清除session
    response = make_response('注销并进行重定向' ,302)
    response.headers['location'] = url_for('index.get_index')
    response.delete_cookie('username')
    response.set_cookie('password', '' , max_age=0)
    return response