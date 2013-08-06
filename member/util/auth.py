# -*- coding: utf-8 -*-

from flask import Flask, session, redirect, request
from member import app
import md5

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
