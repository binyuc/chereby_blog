import os

from flask import Blueprint, render_template, request, session, jsonify
from werkzeug.utils import secure_filename

from module.editor import Editor

editor = Blueprint('editor', __name__)


@editor.route('/editor')
def get_editor():
    return render_template('article_post.html')


@editor.route('/editor-post', methods=['POST'])
def save_blog():
    type = request.form.get('type')
    subtype = request.form.get('subtype')
    articletag = request.form.get('articletag')
    headline = request.form.get('headline')
    # strip 是去除前后的空格
    content = request.form.get('content')
    print('request', content)
    articleid = int(request.form.get('articleid'))
    drafted = int(request.form.get('drafted'))
    checked = int(request.form.get('checked'))
    print('articleid', articleid)
    # 对评论内容进行简单校验
    if session.get('userid') is None:
        return 'perm-denied'
    if len(content) < 5 or len(headline) == 0:
        return 'content-invalid'
    editor = Editor()
    if articleid == 0:
        try:
            id = editor.post(type=type, subtype=subtype, articletag=articletag, headline=headline, content=content, drafted=drafted,
                             checked=checked)
            print('id:', id)
            return str(id)
        except Exception as e:
            return 'add-fail'
    else:
        try:
            id = editor.update(articleid=articleid, type=type, headline=headline, content=content, drafted=drafted,
                               checked=checked)
            print('id:', id)
            return str(id)
        except:
            return 'add-fail'


@editor.route('/admin', methods=['GET'])
def admin():
    if session.get('userid') is None:
        return render_template('error-404.html')
    return render_template('admin.html')


@editor.route('/upload-img', methods=['POST'])
def upload_img():
    global file_name
    if request.method == 'POST':
        fobject = request.files
        print(request.files)
        basedir = os.path.abspath(os.path.join(os.getcwd(), "../"))
        print(basedir)
        res = {
            "errno": 0,
            "data": []
        }
        # TODO 记得切换生产地址
        # base_path = '/root/blogin/blog/resource/pic/article/87'
        # base_path = r'D:\Jupyter\爬虫\blog\resource\pic\article\87'
        base_path = '/root/chereby_blog/resource/pic/article/87'
        for k, v in fobject.items():
            print(k, v)
            file_name = k
            f = v
            img_path = os.path.join(base_path, secure_filename(file_name))
            print(img_path)
            f.save(img_path)
            temp = {
                'url': os.path.join(r'\pic\article\87', secure_filename(file_name)),
                'alt': "图片文字说明",
                'href': "跳转链接"
            }
            res['data'].append(temp)

        return jsonify(res)
