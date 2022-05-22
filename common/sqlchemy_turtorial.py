from sqlalchemy import create_engine,MetaData,Table,Column,Integer,String,DateTime, or_,func, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, session, scoped_session


engine = create_engine('mysql+pymysql://root:mysql123@localhost/blog')

# 定义一个数据链接的会话
DBsession = sessionmaker(bind=engine)
# 多线程
dbsession = scoped_session(DBsession)
Base = declarative_base()
md = MetaData(bind=engine)

# 定义模型类
class Article(Base):
    __table__ = Table('article', md, autoload=True)

class User(Base):
    __table__ = Table('users', md, autoload=True)


if __name__ == '__main__':
    # result = dbsession.query(Article).all()
    # for row in result:
    #     print(row)

    # result = dbsession.query(Article).filter(Article.userid == 1).all()
    # result = dbsession.query(Article).filter_by(userid = 1).first()
    # 返回的是列表
    # print(result)
    #
    # for row in result:
    #     print(row.articleid,)
    # 指定了列名取数
    # result = dbsession.query(Article.type, Article.articleid).filter_by(userid=1).all()
#     # # 通过query 和 filter 进行标准查询
#     # # 返回的是元组
#     # for row in result:
#     #     print(row)
#     新增
#     article = Article(content='hahahhahahhaha',userid=4,type=1,headline='insert header')
#     dbsession.add(article)
#     dbsession.commit() #需要提交,必填项需要完整
    
    # 删除和更新 ： 需要先查询出来要修改的行，在进行修改
    # row = dbsession.query(Article).filter_by(articleid =4).first()
    # row.headline = 'fixed insert header'
    # dbsession.commit()
    
    # 基础查询汇总
    # 通过指定列的方式
    result = dbsession.query(Article).all()  # select * from article
    print(result) #返回的是一个列表(对象)
    
    result = dbsession.query(Article.articleid, Article.type).all()
    print(result[0]) #返回的是列表和元组

    result =dbsession.query(Article).filter_by(articleid = 1, type = 1).all()
    for row in result:
        print(row.headline)

    result =dbsession.query(Article).filter(or_(Article.userid == 1, Article.type ==1 )).all()
    for row in result:
        print(row.headline)

    # 取前三条
    result =dbsession.query(Article).limit(3).all()
    for row in result:
        print(row.headline)

    # 取前5条,从第4条开始
    result =dbsession.query(Article).limit(5).offset(3).all()
    for row in result:
        print('aa',row.headline)

    # 查询数量
    count = dbsession.query(Article).filter(Article.type==1).count()
    print(count)

    # 去重查询
    result = dbsession.query(Article.userid).distinct(Article.articleid).all()
    print(result)

    # 排序 desc
    result = dbsession.query(Article.articleid).order_by(Article.articleid.desc()).all()
    for row in result:
        print(row[0])
    # 模糊匹配
    result = dbsession.query(Article.headline).filter(Article.headline.like('%insert%')).first()
    print(result[0])

    # group by 自动去重了
    result =dbsession.query(Article).group_by(Article.type).having(Article.articleid==1).all()
    for row in result:
        print(row.content)

    # 聚合函数 min ,max , avg, sum
    result = dbsession.query(func.sum(Article.readcount)).first()
    print(result[0])

    # 链接查询
    # 多表链接查询，返回的结果集 不再是单纯的[MODEL,MODEL] 而是[(model1,model2),(model1,model2)]
    result = dbsession.query(Article, User.nickname).join(User, Article.userid == User.userid).filter(User.userid==2).all()
    for article, user in result:
        print('11', user)

    # 外连接,左连接
    result = dbsession.query(User.userid,Article.headline, func.sum(Article.readcount))\
        .outerjoin(Article,User.userid == Article.userid).group_by(Article.userid).all()
    print(result)

    # 复杂查询 and 和 or 混用
    result = dbsession.query(Article).filter(or_(Article.articleid >0) ,and_(Article.headline.like('%insert%'))).first()
    print(result.content)

    result = dbsession.query(Article.type,func.count(Article.articleid))\
        .filter(Article.hidden== 0, Article.drafted== 0,Article.checked==1)\
        .group_by(Article.type).all()
    print(result)

#    根据文章标题进行模糊搜索
    def find_by_aricle_headline(headline, ):
        result = dbsession.query(Article.type, func.count(Article.articleid)) \
            .filter(Article.hidden == 0, Article.drafted == 0, Article.checked == 1, Article.headline.like('% + headline + %')) \
            .order_by(Article.articleid.desc()).limit(count).offset(start).all()
        return result
