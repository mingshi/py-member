# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, redirect, url_for, request, session
from member.util.auth import *
from member.db.db import db_session
from member.model import *
import json

mod = Blueprint("department", __name__)

@mod.route('/department')
def department() :
    if check_admin() :
        departments = db_session.query(Department).all()
        return render_template('member/department.html', departments = departments)
    else :
        return redirect('/403')

@mod.route('/add_department')
def add_department() :
    if check_admin() :
        return render_template('member/add_department.html')
    else :
        return redirect('/403')

@mod.route('/department/do_add', methods=['POST'])
def do_add() :
    if check_admin() :
        result = {}
        if not request.form.has_key('name') :
            result['code'] = 101
            result['msg'] = 'name must be required.'
        else :
            name = request.form['name'].strip().encode('utf8')
            _department = db_session.query(Department).filter_by(name = name).first()
            if _department :
                result['code'] = 102
                result['msg'] = 'the department has been exist.'
            else :
                department = Department(name = name)
                db_session.add(department)
                db_session.commit()
                result['code'] = 0
                result['msg'] = 'add success.'
        return json.dumps(result)
    else :
        return redirect('/403')
