from flask import session, request
from sqlalchemy import Table
from common.database import dbconnect
import time

dbsession, md, DBase = dbconnect()


class Editor(DBase):
    __table__ = Table("article", md, autoload=True)

    # 新增一条博客
    def post(self, type,subtype,articletag, headline, content, drafted =0, checked= 1):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        print(content)
        post_article = Editor(userid=session.get('userid'), type = type, subtype = subtype, tag=articletag ,headline = headline,
                          content=content,  createtime=now, updatetime=now, drafted=drafted, checked=checked)
        dbsession.add(post_article)
        dbsession.commit()
        return post_article.articleid

    def update(self, articleid, type, headline, content, drafted=0, checked=1):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        row = dbsession.query(Editor).filter_by(articleid=articleid).first()
        print(row)
        row.type = type
        row.headline = headline
        row.content = content
        row.drafted = drafted
        row.checked = checked
        row.updatetime = now  # 修改文章的更新时间
        dbsession.commit()
        return str(articleid)  # 继续将文章ID返回调用处