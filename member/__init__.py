# -*- coding: utf-8 -*-

from flask import Flask, send_from_directory, render_template
import os
app = Flask(__name__)

# load config according to enviroment
app.config.from_object("config")
if os.path.exists(app.config['ROOT_PATH'] + "/env.py"):
    app.config.from_object("env")

app.config.from_object("config.%sConfig" % (app.config['ENV']) )

from member.views import index, login, captcha, position, department
from member.db.db import db_session

app.register_blueprint(index.mod)
app.register_blueprint(login.mod)
app.register_blueprint(captcha.mod)
app.register_blueprint(position.mod)
app.register_blueprint(department.mod)

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
