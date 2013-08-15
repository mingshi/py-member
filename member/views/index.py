# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, url_for, redirect, session
from member import app
from member.db.db import db_session
from member.model import *
from member.util.auth import *
from member.util.str import *
import md5
import json

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
        _users = db_session.query(User).join(User.departments,
                User.positions).values(User.id, User.realname, User.email,
                        User.mobile, Position.name, Department.name, User.status,
                        User.is_admin)
        users = []
        for id, realname, email, mobile, name, dname, status, is_admin in _users :
            users.append({'id' : id, 'realname' : realname, 'email' : email,
                'mobile' : mobile, 'pname' : name, 'dname' : dname, 'status' :
                status, 'is_admin' : is_admin})
        #users = db_session.query(User).filter_by(status = 0).all()
        return render_template("member/index.html", users = users) 
    else :
        return redirect("/login")

@mod.route('/user/ajax_position', methods=['POST'])
def ajax_position() :
    result = []
    did = int(request.form['did'])
    _positions = db_session.query(Position).filter_by(did = did).all()
    for _position in _positions :
        result.append({'id' : _position.id, 'name' : _position.name})
    return json.dumps(result)

@mod.route('/user/edit-<id>', methods=['POST','GET'])
def edit_user(id) :
    id = int(id)
    if check_admin() or session['adeazmember_uid'] == id :
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


@mod.route('/user/do_edit', methods=['POST'])
def do_edit_user() :
    id = int(request.form['id'].strip())
    if check_admin() or session['adeazmember_uid'] == id :
        result = {}
        realname = request.form['realname'].strip()
        password = request.form['password'].strip()
        mobile = request.form['mobile'].strip()
        email = request.form['email'].strip()
        department = int(request.form['department'].strip())
        position = int(request.form['position'].strip())

        if not realname :
            result['code'] = 101
            result['msg'] = 'realname must be required.'
        elif password and not check_password(password) :
            result['code'] = 102
            result['msg'] = 'password must be in 8-20 length.'
        elif password and not safe_password(password) :
            result['code'] = 108
            result['msg'] = 'password error,must require alphabet & number & special symbols'
        elif not check_mobile(mobile) :
            result['code'] = 103
            result['msg'] = 'mobile must be in 11 length.'
        elif not check_email(email) :
            result['code'] = 104
            result['msg'] = 'email error.'
        elif department == 0 :
            result['code'] = 105
            result['msg'] = 'department must be required.'
        elif position == 0 :
            result['code'] = 106
            result['msg'] = 'position must be required.'
        elif not id :
            result['code'] = 107
            result['msg'] = 'invalid id.'
        else :
            _user = db_session.query(User).filter_by(id = id).first()
            if password :
                _user.password = md5.new(password).hexdigest()
            _user.realname = realname
            _user.mobile = mobile
            _user.email = email
            _user.department = department
            _user.position = position
            db_session.commit()
            result['code'] = 0
            result['msg'] = 'edit success.'
        
        return json.dumps(result)
    else :
        return redirect('/403')

@mod.route('/user/add')
def add_user() :
    _departments = db_session.query(Department).all()
    return render_template('member/add_user.html', departments = _departments) 

@mod.route('/user/do_add', methods=['POST'])
def do_add_user() :
    result = {}
    realname = request.form['realname'].strip()
    username = request.form['username'].strip()
    password = request.form['password'].strip()
    mobile = request.form['mobile'].strip()
    email = request.form['email'].strip()
    department = int(request.form['department'].strip())
    position = int(request.form['position'].strip())
        
    _user = db_session.query(User).filter_by(username = username).first()
        
    if not realname :
        result['code'] = 101
        result['msg'] = 'realname must be required.'
    elif not check_password(password) :
        result['code'] = 102
        result['msg'] = 'password must be in 8-20 length.'
    elif password and not safe_password(password) :
        result['code'] = 108
        result['msg'] = 'password error,must require alphabet & number & special symbols'
    elif not check_mobile(mobile) :
        result['code'] = 103
        result['msg'] = 'mobile must be in 11 length.'
    elif not check_email(email) :
        result['code'] = 104
        result['msg'] = 'email error.'
    elif department == 0 :
        result['code'] = 105
        result['msg'] = 'department must be required.'
    elif position == 0 :
        result['code'] = 106
        result['msg'] = 'position must be required.'
    elif not username :
        result['code'] = 107
        result['msg'] = 'username must be required.'
    elif _user :
        result['code'] = 109
        result['msg'] = 'the username has been exist.'
    else :
         user = User(username = username, realname = realname, mobile =
                 mobile, email = email, department = department, position =
                 position,status = 0, password =
                 md5.new(password).hexdigest(), is_admin = 0)
         db_session.add(user)
         db_session.commit()
         result['code'] = 0
         result['msg'] = 'add success.'
    return json.dumps(result)

@mod.route('/user/del-<id>', methods=['POST'])
def del_user(id) :
    if check_admin() :
        result = {}
        id = int(id)
        _user = db_session.query(User).filter_by(id = id).first()
        if not _user :
            result['code'] = 103
            result['msg'] = 'invalid id.'
        else :
            _user.status = 1
            db_session.commit()
            result['code'] = 0
            result['msg'] = 'del success.'
        return json.dumps(result)
    else :
        return redirect('/403')
