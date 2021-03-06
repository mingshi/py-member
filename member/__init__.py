# -*- coding: utf-8 -*-

from flask import Flask, request, redirect, send_from_directory, render_template
import os
import re

app = Flask(__name__)

# load config according to enviroment
app.config.from_object("config")
if os.path.exists(app.config['ROOT_PATH'] + "/env.py"):
    app.config.from_object("env")

app.config.from_object("config.%sConfig" % (app.config['ENV']) )

from member.views import index, login, captcha, position, department
from member.views.api import apilogin
from member.views.api import apiuserinfo
from member.views.api import apimultiuserinfo
from member.views.api import userinfo_by_username
from member.views.api import apisearchuser
from member.db.db import db_session
from member.util.auth import *
from member.model.user import User

app.register_blueprint(index.mod)
app.register_blueprint(login.mod)
app.register_blueprint(captcha.mod)
app.register_blueprint(position.mod)
app.register_blueprint(department.mod)
app.register_blueprint(apilogin.mod)
app.register_blueprint(apiuserinfo.mod)
app.register_blueprint(apimultiuserinfo.mod)
app.register_blueprint(userinfo_by_username.mod)
app.register_blueprint(apisearchuser.mod)

@app.before_request
def before_request() :
    path = request.path
    for tmpPath in app.config['NEED_CHECK_ADMIN'] :
        if re.search(tmpPath, path) :
            key = app.config['LOGIN_SESSION_NAME']
            if "'" + key + "'" in session :
                if not check_admin() :
                    return redirect('/403')
            else :
                return redirect('/login')
    if "adeazmember_uid" in session and path == "/" :
        _user = db_session.query(User).filter_by(id = session['adeazmember_uid']).first()
        if _user.is_default_pass == 1 :
            return redirect('/user/edit-' + str(session['adeazmember_uid']))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('member/404.html')

@app.errorhandler(405)
def page_not_found(error):
    return render_template('member/405.html')

@app.route("/version")
def hello():
    return "0.1"

@app.route("/403")
def forbbiden():
    return render_template('member/403.html')

@app.route('/app-path')
def app_path():
    return app.root_path


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static' ), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.teardown_request
def close_session(exception):
    db_session.remove()
