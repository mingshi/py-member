# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, url_for, redirect, session
from member import app
from member.db.db import db_session
from member.model import *

mod = Blueprint("index", __name__)

@mod.route('/')
def index():
    key = app.config['LOGIN_SESSION_NAME']
    if "'" + key + "'" in session :
        '''
        check the user if denied
        '''
        for status in db_session.query(User.status).filter_by(username = session["'" + key + "'"]).first():
            if status == 1 :
                return redirect('/logout')
        users = db_session.query(User).filter_by(status = 0).all()
        return render_template("member/index.html", users = users) 
    else :
        return redirect("/login")
