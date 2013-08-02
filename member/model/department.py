# -*- coding: utf-8 -*-
from member.db.db import Model
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, backref
from member.model.position import Position
from member.model.user import User

class Department(Model):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), info={'name' : 'dname'})
    dname = relationship(Position, backref="departments")
    udname = relationship(User, backref="departments")

    def __init__(self, name) :
        self.name = name

    def __repr__(self) :
        return '<Position %r' % (str(self.id) + ":" + self.name)
