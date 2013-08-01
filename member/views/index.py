# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, url_for, redirect, session
from member import app
from member.db.db import db_session
from member.model import *
from member.util.auth import *

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

@mod.route('/user/edit-<id>', methods=['POST','GET'])
def edit_user(id) :
    if check_admin() :
        id = int(id)
        _user = db_session.query(User).filter_by(id = id).first()
        _departments = db_session.query(Department).all()
        _positions = db_session.query(Position).all()
        _position = db_session.query(Position).filter_by(id = _user.position).first()

        if not _user :
            return redirect('/403')
        else :
            return render_template('member/edit_user.html', user = _user,
                    departments = _departments, positions = _positions, position = _position)
    else :
        return redirect('/403')
