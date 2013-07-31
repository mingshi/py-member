# -*- coding: utf-8 -*-

from flask import Blueprint, Response, session
from member.util.captcha import *
import StringIO
from member import app

mod = Blueprint("captcha", __name__)

@mod.route('/captcha')
def captcha():
    app.secret_key = app.config['SECRET_KEY']
    res = create()
    image = res['image']
    SESSION_KEY_CAPTCHA = app.config['SESSION_KEY_CAPTCHA']
    session["'" + SESSION_KEY_CAPTCHA + "'"] = res['chars']
    buf = StringIO.StringIO()
    image.save(buf,'png',quality=70)
    return Response(buf.getvalue(), mimetype='image/png')
