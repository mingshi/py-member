#!/usr/bin/env python
# -*- coding: utf-8 -*-
from member.db.db import init_db, db_session

if __name__ == "__main__":
    print "bwgin inited db \n"
    init_db()

    from member.model.user import User
    from member.model.position import Position
    from member.mode.department import Department

    #memcache = Memcacheds(ip='192.168.1.96', port=11212, status=1, group_id =1,version='1.4.0')
    #db_session.add(memcache)
    #db_session.commit()

    print "inited db end \n"
