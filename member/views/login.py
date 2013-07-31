# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, redirect, url_for, request, session
from member.db.db import db_session
import json
from member.model import *
from member import app
import time

mod = Blueprint("login", __name__)

@mod.route('/login')
def login():
    username = request.cookies.get('m_username')
    if not username :
        return render_template('member/login.html')
    else :
        return redirect(url_for("index.index"))


@mod.route('/do_login', methods=['POST'])
def do_login():
    result = {}
    if not request.form.has_key('username') :
        result['code'] = 101
        result['msg'] = 'username must be required!'
    elif not request.form.has_key('password') :
        result['code'] = 102
        result['msg'] = 'password must be required!'
    elif not request.form.has_key('verify') :
        result['code'] = 103
        result['msg'] = 'verify must be required!'
    else :
        verify = request.form['verify'].strip().encode('utf8')
        username = request.form['username'].strip().encode('utf8')
        password = request.form['password'].strip().encode('utf8')
        
        SESSION_KEY_CAPTCHA = app.config['SESSION_KEY_CAPTCHA']
        tmpVerify = session["'" + SESSION_KEY_CAPTCHA + "'"]
        _user = db_session.query(User).filter_by(username = username).first()
        code = ""

        for _code in tmpVerify :
            code += _code
        code = code.lower()
        
        if not session["'" + SESSION_KEY_CAPTCHA + "'"] :
            result['code'] = 105
            result['msg'] = 'session error for captcha!'
        elif not verify == code :
            result['code'] = 106
            result['msg'] = 'verify error!'
        elif not _user :
            result['code'] = 104
            result['msg'] = 'user not exist!'
        elif not password == _user.password :
            result['code'] = 107
            result['msg'] = 'password error!'
        elif _user.status == app.config['USER_STATUS_DELETE'] :
            result['code'] = 109
            result['msg'] = 'user has been denied!'
        else :
            _user.login_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) 
            db_session.commit()
            key = app.config['LOGIN_SESSION_NAME']
            session["'" + key + "'"] = username
            session['adeazmember_realname'] = _user.realname
            if _user.is_admin == 1 :
                session['member_is_admin'] = 1
            result['code'] = 0
            result['msg'] = 'login success!'
    return json.dumps(result)

@mod.route('/logout')
def logout() :
    key = app.config['LOGIN_SESSION_NAME']
    session.pop("'" + key + "'", None)
    session.pop('adeazmember_realname', None)
    if 'member_is_admin' in session :
        session.pop('member_is_admin', None)
    
    return redirect('/')
