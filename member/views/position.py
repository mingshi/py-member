# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, redirect, url_for, request, session
from member.util.auth import *
from member.db.db import db_session
from member.model import *
import json

mod = Blueprint("position", __name__)

@mod.route('/position')
def position() :
    if check_admin() :
        _positions = db_session.query(Position).join(Position.departments).values(Position.id, Position.name, Position.did, Department.name)
        positions = []
        for id, name, did,dname in _positions :
            positions.append({'id' : id, 'name' : name, 'did' : did, 'dname' : dname})
        return render_template('member/position.html', positions = positions)
    else :
        return redirect('/403')

@mod.route('/position/edit-<id>')
def edit_position(id) :
    if check_admin() :
        _position = db_session.query(Position).filter_by(id = id).first()
        _departments = db_session.query(Department).all()
        return render_template('member/edit_position.html', position = _position, departments = _departments)
    else :
        return redirect('/403')

@mod.route('/position/do_edit', methods=['POST'])
def do_edit_position() :
    if check_admin() :
        result = {}
        if not request.form.has_key('id') :
            result['code'] = 101
            result['msg'] = 'id must be required.'
        elif not request.form.has_key('name') :
            result['code'] = 102
            result['msg'] = 'name must be required.'
        elif not request.form.has_key('did') :
            result['code'] = 103
            result['msg'] = 'department must be required.'
        else :
            name = request.form['name'].strip()
            id = int(request.form['id'].strip())
            did = int(request.form['did'].strip())
            _position = db_session.query(Position).filter_by(id = id).first()
            if _position :
                _position.name = name
                _position.did = did
                db_session.commit()
                result['code'] = 0
                result['msg'] = 'edit success.'
            else :
                result['code'] = 104
                result['msg'] = 'invalid id.'
        return json.dumps(result)
    else :
        return redirect('/403')

@mod.route('/position/del-<id>', methods=['POST'])
def del_position(id) :
    if check_admin() :
        result = {}
        id = int(id)
        _position = db_session.query(Position).filter_by(id = id).first()
        db_session.delete(_position)
        db_session.commit()
        result['code'] = 0
        result['msg'] = 'del success'
        return json.dumps(result)
    else :
        return redirect('/403')

@mod.route('/position/add')
def add_position() :
    if check_admin() :
        _departments = db_session.query(Department).all()
        return render_template('member/add_position.html', departments = _departments)
    else :
        return redirect('/403')

@mod.route('/position/do_add', methods=['POST'])
def do_add_position() :
    if check_admin() :
        result = {}
        if not request.form.has_key('name') :
            result['code'] = 101
            result['msg'] = 'name must be required.'
        elif not request.form.has_key('did') :
            result['code'] = 102
            result['msg'] = 'department must be required.'
        else :
            name = request.form['name'].strip()
            did = int(request.form['did'].strip())
            _position = db_session.query(Position).filter_by(did = did, name = name).first()
            if _position :
                result['code'] = 103
                result['msg'] = 'the position has been exist in this department.'
            else :
                position = Position(name = name, did = did)
                db_session.add(position)
                db_session.commit()
                result['code'] = 0
                result['msg'] = 'add success.'
        return json.dumps(result)
    else :
        return redirect('/403')
