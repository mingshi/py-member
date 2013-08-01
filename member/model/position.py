# -*- coding: utf-8 -*-
from member.db.db import Model
from sqlalchemy import Column, Integer, String, ForeignKey

class Position(Model):
    __tablename__ = 'position'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    did = Column(Integer, ForeignKey('department.id'), nullable=False)

    def __init__(self, name, did) :
        self.name = name
        self.did = did

    def __repr__(self) :
        return '<Position %r' % (str(self.id) + ":" + self.name)
