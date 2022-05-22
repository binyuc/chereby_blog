import time
from flask import jsonify
from common.database import dbconnect
# from main import db
from sqlalchemy import Table, MetaData,func

dbsession, md, DBase = dbconnect()


# 所有数据库的操作放在module
class Article(DBase):
    __table__ = Table('article', md, autoload=True)

    def find_all(self):
        result = dbsession.query(Article).all()
        return result

    def find_by_id(self, articleid):
        row = dbsession.query(Article).filter(Article.articleid == articleid).first()
        return row

    # 指定分页
    def find_limit_with_article(self, start, count):
        result = dbsession.query(Article)\
            .filter(Article.hidden== 0, Article.drafted== 0,Article.checked==1)\
            .order_by(Article.articleid.desc()).limit(count). \
            offset(start).all()
        return result

    # 获取总数量
    def get_total_count(self):
        count = dbsession.query(Article).filter(Article.hidden== 0, Article.drafted== 0,Article.checked==1).count()
        return count

    # 根据分类查找
    def find_by_type(self,type, start,count):
        result = dbsession.query(Article)\
            .filter(Article.hidden== 0, Article.drafted== 0,Article.checked==1,Article.type==type)\
            .order_by(Article.articleid.desc()).order_by(Article.articleid.desc()).limit(count). \
            offset(start).all()
        return result

    # 根据分类查找个数
    def get_count_by_type(self,type):
        count = dbsession.query(Article).filter(Article.hidden== 0, Article.drafted== 0,Article.checked==1, Article.type==type).count()
        return count

    # 根据文章标题模糊搜索
    def find_by_aricle_headline(self,headline, start,count):
        result = dbsession.query(Article) \
            .filter(Article.hidden == 0, Article.drafted == 0, Article.checked == 1, Article.headline.like('%' + headline + '%')) \
            .order_by(Article.articleid.desc()).limit(count).offset(start).all()
        return result

    # 统计标题搜索后的分页数量
    def get_count_by_headline(self,headline):
        count = dbsession.query(Article).filter(Article.hidden == 0, Article.drafted == 0, Article.checked == 1,
                                                Article.headline.like('%' + headline + '%')).count()
        return count

    # 当发表或者回复评论后，为文章表的字段replycount 加1
    def update_replycount(self, articleid):
        row = dbsession.query(Article).filter_by(articleid=articleid).first()
        row.replycount+=1
        dbsession.commit()

    # 更新一次阅读次数
    def update_read_count(self,articleid):
        row = dbsession.query(Article).filter_by(articleid=articleid).first()
        row.readcount += 1
        dbsession.commit()

    # 根据分类查找
    def find_by_subtype(self,type, subtype, start,count):
        result = dbsession.query(Article)\
            .filter(Article.hidden== 0, Article.drafted== 0,Article.checked==1,Article.subtype==subtype,Article.type==type)\
            .order_by(Article.articleid.desc()).order_by(Article.articleid.desc()).limit(count). \
            offset(start).all()
        return result

    # 根据分类查找个数
    def get_count_by_subtype(self,type,subtype):
        count = dbsession.query(Article).filter(Article.hidden== 0, Article.drafted== 0,Article.checked==1,Article.type==type,Article.subtype==subtype).count()
        return count

    # 找到各个分类以及分类下的文章数量
    def find_count_by_type(self):
        result = dbsession.query(Article.type, func.count(Article.articleid)) \
            .filter(Article.hidden == 0, Article.drafted == 0, Article.checked == 1) \
            .group_by(Article.type).all()
        return result

    # 找到子分类下的文章
    def find_count_by_subtype(self):
        result = dbsession.query(Article.type, Article.subtype, func.count(Article.articleid)) \
            .filter(Article.hidden == 0, Article.drafted == 0, Article.checked == 1) \
            .group_by(Article.type, Article.subtype).order_by(Article.type).all()
        dic = {
            '1': [],
            '2': [],
            '3': [],
            '4': [],
            '5': [],
            '6': [],
            '7': [],
        }
        for row in result:
            for k, v in dic.items():
                if str(row[0]) == k:
                    temp = {str(row[1]): row[2]}
                    v.append(temp)
        return dic


