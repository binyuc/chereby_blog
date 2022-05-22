from sqlalchemy import Table, func

from common.database import dbconnect

dbsession, md, DBase = dbconnect()


# 所有数据库的操作放在module
class Index(DBase):
    __table__ = Table('article', md, autoload=True)

    def find_all(self):
        result = dbsession.query(Index).all()
        return result

    def find_by_id(self, articleid):
        row = dbsession.query(Index).filter(Index.articleid == articleid).first()
        return row

    # 指定分页
    def find_limit_with_article(self, start, count):
        result = dbsession.query(Index).order_by(Index.articleid.desc()).limit(count). \
            offset(start).all()
        return result

    def find_limit_with_article_popular(self, start, count):
        result = dbsession.query(Index).order_by(Index.readcount.desc()).limit(count). \
            offset(start).all()
        return result

    # 找到分类下的文章
    def find_by_type(self, type):
        result = dbsession.query(Index) \
            .filter(Index.hidden == 0, Index.drafted == 0, Index.checked == 1, Index.type == type) \
            .order_by(Index.articleid.desc())
        return result

    # 找到各个分类以及分类下的文章数量
    def find_count_by_type(self):
        result = dbsession.query(Index.type, func.count(Index.articleid)) \
            .filter(Index.hidden == 0, Index.drafted == 0, Index.checked == 1) \
            .group_by(Index.type).all()
        return result

    # 找到子分类下的文章
    def find_count_by_subtype(self):
        result = dbsession.query(Index.type, Index.subtype, func.count(Index.articleid)) \
            .filter(Index.hidden == 0, Index.drafted == 0, Index.checked == 1) \
            .group_by(Index.type, Index.subtype).order_by(Index.type).all()
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


Index().find_count_by_subtype()
