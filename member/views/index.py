# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, url_for, redirect, session
from member import app
from member.db.db import db_session
from member.model import *
from member.util.auth import *
from member.util.str import *
from sqlalchemy import or_
import md5
import json
from flask.ext.sqlalchemy import Pagination
import math

mod = Blueprint("index", __name__)

@mod.route('/', methods=['GET','POST'])
def index():
    key = app.config['LOGIN_SESSION_NAME']
    if "'" + key + "'" in session :
        '''
        check the user if denied
        '''
        for status in db_session.query(User.status).filter_by(username = session["'" + key + "'"]).first():
            if status == 1 :
                return redirect('/logout')

        kw = request.args.get('kw')
        query_string = ""
        if kw and kw.strip():
            query_string = "kw=" + kw
            _users = db_session.query(User).join(User.departments, User.positions).filter(or_(User.mobile.like('%' + kw + '%'), User.realname.like('%' + kw + '%'), User.email.like('%' + kw + '%'))).values(User.id, User.realname, User.email, User.qq, User.mobile, Position.name, Department.name, User.status, User.is_admin) 
        else :
            _users = db_session.query(User).join(User.departments,
                    User.positions).values(User.id, User.realname, User.email, User.qq,
                            User.mobile, Position.name, Department.name, User.status,
                            User.is_admin)
        users = []
        for id, realname, email, qq, mobile, name, dname, status, is_admin in _users :
            users.append({'id' : id, 'realname' : realname, 'email' : email, 'qq' : qq,
                'mobile' : mobile, 'pname' : name, 'dname' : dname, 'status' :
                status, 'is_admin' : is_admin})
        #users = db_session.query(User).filter_by(status = 0).all()
     
        currentUrl = request.url
        allNum = len(users)
        per_page = 10
        pages = int(math.ceil(float(allNum) / per_page))

        if not request.args.get('page') :
            page = 1
        else :
            page = int(request.args.get('page'))

        if page < 0 or (len(users) > 0 and page > pages) :
            return redirect('/404')
       
        start = (page - 1) * per_page
        end = page * per_page
        users = users[start : end]
        pagination = Pagination(None, page, per_page, int(allNum), None)

        #get my info
        myId = session['adeazmember_uid']
        _myInfo = db_session.query(User).join(User.departments, User.positions).filter(User.id == myId).values(User.id, User.realname, User.email, User.qq, User.mobile, User.login_time, User.login_ip, Position.name, Department.name, User.status, User.is_admin, User.status)
        myInfo = {}
        for id, realname, email,qq, mobile, login_time, login_ip,name, dname, status, is_admin, status in _myInfo :
            myInfo['id'] = id
            myInfo['realname'] = realname
            myInfo['email'] = email
            myInfo['mobile'] = mobile
            myInfo['position'] = name
            myInfo['department'] = dname
            myInfo['status'] = status
            myInfo['is_admin'] = is_admin
            myInfo['login_time'] = str(login_time)
            myInfo['login_ip'] = login_ip
            myInfo['status'] = status
            myInfo['qq'] = qq
        


        return render_template("member/index.html", users = users, myInfo = myInfo, pagination = pagination, query_string = query_string) 
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
            higherUserStr = ""
            higher = int(_user.higher)
            higherUser = db_session.query(User).filter_by(id = higher).first()
            if higherUser :
                higherUserPosition = db_session.query(Position).filter_by(id = higherUser.higher).first()
                if higherUserPosition :
                    higherUserStr = str(higherUser.id) + " " + higherUser.realname + " " + higherUserPosition.name
                else :
                    higherUserStr = str(higherUser.id) + " " + higherUser.realname

            return render_template('member/edit_user.html', user = _user,
                    departments = _departments, positions = _positions, position = _position, higherUserStr = higherUserStr)
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
        qq = request.form['qq'].strip()
        department = int(request.form['department'].strip())
        position = int(request.form['position'].strip())
        higher = request.form['higher'].strip()
        hArr = higher.split(' ')
        higherUid = hArr[0]
        if not higherUid :
            higherUid = 0

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
            _user.qq = qq
            _user.higher = higherUid
            if _user.is_default_pass == 1 :
                _user.is_default_pass = 0
            session['adeazmember_realname'] = realname
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
    qq = request.form['qq'].strip()
    department = int(request.form['department'].strip())
    position = int(request.form['position'].strip())
    higher = request.form['higher'].strip()
    hArr = higher.split(' ')
    higherUid = hArr[0]
    if not higherUid :
        higherUid = 0

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
                 mobile, email = email, qq = qq, department = department, position =
                 position,status = 0, password =
                 md5.new(password).hexdigest(), is_admin = 0, is_default_pass = 1, higher = higherUid)
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

@mod.route('/user/restore-<id>', methods=['POST'])
def restore_user(id) :
    if check_admin() :
        result = {}
        id = int(id)
        _user = db_session.query(User).filter_by(id = id).first()
        if not _user :
            result['code'] = 103
            result['msg'] = 'invalid id.'
        else :
            _user.status = 0
            db_session.commit()
            result['code'] = 0
            result['msg'] = 'restore success.'
        return json.dumps(result)
    else :
        return redirect('/403')

@mod.route('/getJsonUser', methods=['GET'])
def get_json_user() :
    kwd = request.args.get('term').strip()
    _user = db_session.query(User).join(User.departments, User.positions).filter(User.email.like('%' + kwd + '%')).values(User.id, User.realname, User.higher, Position.name, Department.name)
    users = []
    for id, realname, name, dname, higher in _user :
        user = {}
        user['id'] = id
        user['realname'] = realname
        user['position'] = name
        user['department'] = dname
        user['label'] = str(id) + " " + realname + " " + dname
        user['value'] = str(id) + " " + realname + " " + dname
        user['higher'] = higher
        users.append(user)

    return json.dumps(users)
