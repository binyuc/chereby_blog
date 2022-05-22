from flask import jsonify
from common.database import dbconnect
from main import db
from sqlalchemy import Table, MetaData, func

dbsession, md, DBase = dbconnect()

# 所有数据库的操作放在module
class User(DBase):
    __table__ = Table('users',md ,autoload=True)

    def find_by_username(self,username):
        result = dbsession.query(User).filter(User.username == username).all()
        return result