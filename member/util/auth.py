# -*- coding: utf-8 -*-

from flask import Flask, session, redirect, request
from member import app
import md5
import re

def check_admin() :
    if ('member_is_admin' in session) and (session['member_is_admin'] == 1) :
        return "1"
    else :
        return None

def create_login_sign() :
    params = []
    for key in request.form :
        params.append(key)
    params.append("key")
    params.sort()
   
    uri = ""
    for _key in params :
        if (_key == "sign") :
            continue
        if (_key == "key") :
            _value = app.config['LOGIN_KEY']
        else :
            _value = request.form[_key]
        
        uri += _key + "=" + _value + "&"
    uri = uri.strip('&')
    sign = md5.new(uri).hexdigest()

    return sign

def create_user_info_sign() :
    sign = md5.new("key=" + app.config['USER_INFO_KEY'] + "&uid=" + str(request.form['uid'].strip())).hexdigest()
    return sign


def safe_password(str) :
    level = 0;
    if re.search('\d', str) :
        level += 1
    if re.search('[a-z]', str) :
        level += 1
    if re.search('[A-Z]', str) :
        level += 1
    if re.search('[^0-9a-zA-Z]', str) :
        level += 1

    if level < 3 :
        return None
    return 1
