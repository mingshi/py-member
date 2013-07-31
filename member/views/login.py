# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, redirect, url_for, request, session
from member.db.db import db_session
import json
from member.model import *
from member import app

mod = Blueprint("login", __name__)

@mod.route('/login')
def login():
    username = request.cookies.get('m_username')
    if not username :
        return render_template('member/login.html')
    else :
        return redirect(url_for("index.index"))


@mod.route('/do_login', methods=['GET','POST'])
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
        else :
            key = app.config['LOGIN_SESSION_NAME']
            session["'" + key + "'"] = username
            session['adeazmember_realname'] = _user.realname
            result['code'] = 0
            result['msg'] = 'login success!'
    return json.dumps(result)

@mod.route('/logout')
def logout() :
    key = app.config['LOGIN_SESSION_NAME']
    session.pop("'" + key + "'", None)
    session.pop('adeazmember_realname', None)
    return redirect('/')
