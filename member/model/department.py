# -*- coding: utf-8 -*-
from member.db.db import Model
from sqlalchemy import Column, Integer, String

class Department(Model):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))

    def __init__(self, name) :
        self.name = name

    def __repr__(self) :
        return '<Position %r' % (self.id + ":" + self.name)
