# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, redirect, url_for, request

mod = Blueprint("memcached", __name__)

@mod.route('/login')
def login():
    username = request.cookies.get('m_username')
    if not username :
        return render_template('member/login.html')
    else :
        return redirect(url_for("index.index"))


@mod.route('/do_login', methods=['GET','POST'])
def do_login():
    return "111"
