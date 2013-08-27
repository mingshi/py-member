# -*- coding: utf-8 -*-
from member.db.db import Model
from sqlalchemy import Column, Integer, String, ForeignKey

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
    is_admin = Column(Integer)
    position = Column(Integer, ForeignKey('position.id'), nullable=False)
    department = Column(Integer, ForeignKey('department.id'), nullable=False)
    is_default_pass = Column(Integer)

    def __init__(self, username, realname, password, mobile, email, status, department, position, is_admin):
        self.username = username
        self.realname = realname
        self.password = password
        self.mobile = mobile
        self.email = email
        self.status = status
        self.department = department
        self.position = position
        self.is_admin = is_admin

    def __repr__(self):
        return '<User %r' % (self.username + ":" + self.realname)

