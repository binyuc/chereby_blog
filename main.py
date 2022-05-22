import itertools

from flask import Flask, make_response, g
from flask import render_template, request, redirect, url_for, session
import os
from flask_sqlalchemy import SQLAlchemy
import pymysql
from datetime import datetime
import logging
pymysql.install_as_MySQLdb()

app = Flask(__name__, static_url_path='/', static_folder='resource/', template_folder='template')
app.config['SECRET_KEY'] = os.urandom(24)  # 生产随机数种子，用于生产session id
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql123@localhost:3306/blog?charset=utf8'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://oper:CBYcby8587858=@43.129.220.213:3306/blog?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # True: 跟踪数据库的修改，及时发送信号
app.config['SQLALCHEMY_POOL_SIZE'] = 100  # 数据库连接池的大小。默认是数据库引擎的默认值（通常是 5）
db = SQLAlchemy(app)

# 日志系统配置
handler = logging.FileHandler('blog.log', encoding='UTF-8')
#设置日志文件，和字符编码
logging_format = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
handler.setFormatter(logging_format)
app.logger.addHandler(handler)


# 定义404错误页面
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error-404.html')

# 定义500错误页面
@app.errorhandler(500)
def server_error(e):
    return render_template('error-500.html')


# 定义文章类型
@app.context_processor
def gen_article_type():
    article_type = {
        '1': '数据分析',
        '2': '机器学习',
        '3': '应用及部署',
        '4': '行业见解',
        '5': '网络爬虫',
        '6': '心得备忘录',
        '7': '小工具',
    }
    return dict(article_type=article_type)

# 自定义过滤器来重构
def mytruncate(s, length, end='...'):
    count = 0
    new = ''
    for c in s:
        new += c
        if ord(c) < 128:
            count += 0.5
        else:
            count += 1
        if count > length:
            break
    return new + end


# 注册过滤器
app.jinja_env.filters.update(mytruncate=mytruncate)


@app.before_request
# 全局拦截器，判断是否session里是不是有 islogin, 实现自动登录
def before():
    url = request.path
    pass_list = ['/logout']
    if url in pass_list or url.endswith('.js') or url.endswith('.jpg') or url.endswith('jepg'):
        pass
    if session.get('islogin') is None:
        username = request.cookies.get('username')
        password = request.cookies.get('password')
        if username != None and password != None:
            user = User()
            result = user.find_by_username(username)
            if len(result) == 1 and result[0].password == password:
                session['islogin'] = 'true'
                session['userid'] = result[0].userid
                session['username'] = username
                session['nickname'] = result[0].nickname
                session['role'] = result[0].role
    app.logger.info(request.headers)
    #     自动登录的话，登录一次就会更新一次cookie，那么cookie永远就不会过期


# # TODO 这里部署前也需要修改
from controller.article import *
app.register_blueprint(article)
from controller.index import *
app.register_blueprint(index)
from controller.editor import *
app.register_blueprint(editor)
from controller.user import *
app.register_blueprint(user)
from controller.comment import *
app.register_blueprint(comment)
from controller.editor import *
app.register_blueprint(editor)
from controller.fun import *
app.register_blueprint(fun)
from controller.poker import *
app.register_blueprint(poker)


# if __name__ == '__main__':
#     from controller.article import *
#     app.register_blueprint(article)
#     from controller.index import *
#     app.register_blueprint(index)
#     from controller.editor import *
#     app.register_blueprint(editor)
#     from controller.user import *
#     app.register_blueprint(user)
#     from controller.comment import *
#     app.register_blueprint(comment)
#     from controller.editor import *
#     app.register_blueprint(editor)
#     from controller.fun import *
#     app.register_blueprint(fun)
#     from controller.poker import *
#     app.register_blueprint(poker)
#     app.run(debug=True, host="127.0.0.1", port=5001)


