# -*- coding: utf-8 -*-
from member.db.db import Model
from sqlalchemy import Column, Integer, String

class User(Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True)
    realname = Column(String(50))
    password = Column(String(32))
    mobile = Column(String(20))
    email = Column(String(50))
    status = Column(Integer)
    login_time = Column(String(19))
    login_ip = Column(String(15))

    def __init__(self, username, realname, password, mobile, email, status, login_time, login_ip):
        self.username = username
        self.realname = realname
        self.password = password
        self.mobile = mobile
        self.email = email
        self.status = status
        self.login_time = login_time
        self.login_ip = login_ip

    def __repr__(self):
        return '<User %r' % (self.username + ":" + self.realname)

