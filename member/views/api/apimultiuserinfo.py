# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, redirect, url_for, request, session
from member.db.db import db_session
from member.model import *
from member.util.auth import *
from member import app
import json

mod = Blueprint("apimultiuserinfo", __name__)

@mod.route('/api/apimultiuserinfo', methods=['POST'])
def api_multiuserinfo() :
    result = {}
    try :
        if not request.form.has_key('key') :
            result['code'] = 101
            result['msg'] = '密钥是必须的'
        elif not request.form.has_key('uid') :
            result['code'] = 102
            result['msg'] = '用户id是必须的'
        elif not request.form.has_key('sign') :
            result['code'] = 103
            result['msg'] = '签名是必须的'
        elif not request.form['key'] == app.config['USER_INFO_SIGN'] :
            result['code'] = 104
            result['msg'] = '密钥错误'
        elif not request.form['sign'] == create_user_info_sign() :
            result['code'] = 105
            result['msg'] = '签名错误'
        else :
            uid = request.form['uid'].strip()
            _users = db_session.query(User).join(User.departments, User.positions).filter(User.id.in_(uid)).values(User.id, User.realname, User.email, User.qq, User.mobile, User.login_time, User.login_ip, Position.name, Department.name, User.status, User.is_admin, User.status)
            print(_users)
            users = []
            for id, realname, email,qq, mobile, login_time, login_ip,name, dname, status, is_admin, status in _users :
                users.append({
                    'id'    :   id,
                    'realname'  :   realname,
                    'email' :   email,
                    'mobile'    :   mobile,
                    'position'  :   name,
                    'department'    :   dname,
                    'status'    :   status,
                    'is_admin'  :   is_admin,
                    'login_time'    :   str(login_time),
                    'login_ip'  :   login_ip,
                    'qq'    :   qq
                });
            
            result['code'] = 0
            result['msg'] = 'success'
            result['info'] = users
    except Exception, e :
        result['code'] = 155
        result['msg'] = '系统错误'

    if not result['code'] == 0 :
        result['status'] = 'err'
    else :
        result['status'] = 'ok'
    return json.dumps(result)
