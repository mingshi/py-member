# -*- coding: utf-8 -*-

'''
Author  :   Mingshi <fivemingshi@gmail.com>
Created :   2014/01/07 11:30:43
FileName:   apisearchuser.py
'''
from flask import Blueprint, render_template, request, redirect, url_for, request, session
from member.db.db import db_session
from member.model import *
from member.util.auth import *
from member import app
import json

mod = Blueprint("apisearchuser", __name__)

@mod.route('/api/apisearchuser', methods=['POST'])
def apisearchuser() :
    result = {}
    try :
        if not request.form.has_key('key') :
            result['code'] = 101
            result['msg'] = '密钥是必须的'
        elif not request.form.has_key('kwd') :
            result['code'] = 102
            result['msg'] = '关键词是必须的'
        elif not request.form.has_key('sign') :
            result['code'] = 103
            result['msg'] = '签名是必须的'
        elif not request.form['key'] == app.config["SEARCH_USER_KEY"] :
            result['code'] = 104
            result['msg'] = '密钥错误'
        elif not request.form['sign'] == create_search_user_sign() :
            result['code'] = 105
            result['msg'] = '签名错误'
        else :
            kwd = str(request.form['kwd']).strip()
            _user = db_session.query(User).join(User.departments, User.positions).filter(User.email.like('%' + kw + '%')).values(User.id, User.realname, Position.name, Department.name)
            user = {}
            for id, realname, name, dname in _user :
                user['id'] = id
                user['realname'] = realname
                user['position'] = name
                user['department'] = dname
                user['label'] = "\""+ str(id) + " " + realname + " " + dname + "\""
                user['value'] = "\""+ str(id) + " " + realname + " " + dname + "\""
            

            result['code'] = 0
            result['msg'] = 'success'
            result['info'] = user
    except Exception, e :
        result['code'] = 155
        result['msg'] = '系统错误'
    if not result['code'] == 0 :
        result['status'] = 'err'
    else :
        result['status'] = 'ok'
    return json.dumps(result)

