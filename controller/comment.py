from flask import Blueprint, request
from module.comment import Comment
from module.article import Article

comment = Blueprint('comment', __name__)


@comment.route('/comment', methods=['POST'])
def add():
    articleid = request.form.get('articleid')
    # strip 是去除前后的空格
    content = request.form.get('content').strip()
    ipaddr = request.remote_addr
    tempname = request.form.get('tempname').strip()

    # 对评论内容进行简单校验
    if len(content) < 5 or len(content) > 1000 or len(tempname)==0:
        return 'content-invalid'
    comment = Comment()
    if not comment.check_limit_per_5_ip():
        try:
            comment.insert_comment(articleid, content, ipaddr,tempname)
            Article().update_replycount(articleid)
            return 'add-pass'
        except:
            return 'add-fail'
    else:
        return 'add-limit'

@comment.route('/reply', methods=['POST'])
def reply():
    articleid = request.form.get('articleid')
    commentid = request.form.get('commentid')
    content = request.form.get('content').strip()
    ipaddr = request.remote_addr
    tempname = request.form.get('tempname').strip()

    # # 对评论内容进行简单校验
    if len(content) < 5 or len(content) > 1000 or len(tempname)==0:
        return 'content-invalid'
    comment = Comment()
    # use ip instead of id
    # if not comment.check_limit_per_5_id():
    if not comment.check_limit_per_5_ip():
        try:
            comment.insert_reply(articleid=articleid, commentid=commentid,content=content, ipaddr=ipaddr,tempname=tempname)
            Article().update_replycount(articleid)
            return 'reply-pass'
        except Exception as e:
            # print(e)
            return 'reply-fail'
    else:
        return 'reply-limit'