# -*- coding: utf-8 -*-
from member.db.db import Model
from sqlalchemy import Column, Integer, String

class Position(Model):
    __tablename__ = 'position'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    did = Column(Integer)

    def __init__(self, name, did) :
        self.name = name
        self.did = did

    def __repr__(self) :
        return '<Position %r' % (self.id + ":" + self.name)
