# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, redirect, url_for, request, session
from member.db.db import db_session
from member.model import *
from member.util.auth import *
from member import app
import json

mod = Blueprint("apilogin", __name__)

@mod.route('/api/login', methods=['POST'])
def api_login() :
    result = {}
    try :
        if not request.form.has_key('username') :
            result['code'] = 103
            result['msg'] = '用户名是必须的'
        elif not request.form.has_key('password') :
            result['code'] = 104
            result['msg'] = '密码是必须的'
        elif not request.form.has_key('sign') :
            result['code'] = 105
            result['msg'] = '签名串是必须的'
        elif not request.form['sign'] == create_login_sign() :
            result['code'] = 106
            result['msg'] = '签名错误'
        else :
            username = request.form['username'].strip()
            password = request.form['password'].strip()
            sign = request.form['sign'].strip()
            _user = db_session.query(User).filter_by(username = username).first()
            if not _user :
                result['code'] = 107
                result['msg'] = '用户不存在'
            else :
                sign = app.config['SIG_KEY']
                loginSign = md5.new(str(sign) + str(_user.password)).hexdigest()
                if not password == loginSign :
                    result['code'] = 108
                    result['msg'] = '密码错误'
                elif _user.status == 1 :
                    result['code'] = 109
                    result['msg'] = '用户已禁用'
                else :
                    result['code'] = 0
                    result['msg'] = '登录成功'
                    result['info'] = {}
                    result['info']['username'] = username
                    result['info']['realname'] = _user.realname
                    result['info']['mobile'] = _user.mobile
                    result['info']['email'] = _user.email
                    result['info']['is_admin'] = _user.is_admin
    except Exception, e :
        result['code'] = 155
        result['msg'] = '系统错误'

    if not result['code'] == 0 :
        result['status'] = 'err'
    else :
        result['status'] = 'ok'
    return json.dumps(result)
