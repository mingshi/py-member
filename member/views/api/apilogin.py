# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, redirect, url_for, request, session
from member.db.db import db_session
from member.model import *
from member.util.auth import *
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
            
    except Exception, e :
        result['code'] = 155
        result['msg'] = '系统错误'
    return json.dumps(result)
