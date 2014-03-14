# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, redirect, url_for, request, session
from member.db.db import db_session
from member.model import *
from member.util.auth import *
from member import app
import json

mod = Blueprint("apiuserinfo", __name__)

@mod.route('/api/userinfo', methods=['POST'])
def api_userinfo() :
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
            uid = int(request.form['uid'])
            _user = db_session.query(User).join(User.departments, User.positions).filter(User.id == uid).values(User.id, User.realname, User.email, User.qq, User.mobile, User.login_time, User.login_ip, Position.name, Department.name, User.status, User.is_admin, User.higher)
            user = {}
            for id, realname, email,qq, mobile, login_time, login_ip,name, dname, status, is_admin, higher in _user :
                user['id'] = id
                user['realname'] = realname
                user['email'] = email
                user['mobile'] = mobile
                user['position'] = name
                user['department'] = dname
                user['status'] = status
                user['is_admin'] = is_admin
                user['login_time'] = str(login_time)
                user['login_ip'] = login_ip
                user['qq'] = qq
                user['higher'] = higher

            if not _user :
                result['code'] = 106
                result['msg'] = '用户不存在'
            else :
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

