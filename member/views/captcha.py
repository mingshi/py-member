# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, Response, redirect, url_for
from member.util.captcha import *
import StringIO

mod = Blueprint("captcha", __name__)

@mod.route('/captcha')
def captcha():
    image = create()
    buf = StringIO.StringIO()
    image.save(buf,'png',quality=70)
    return Response(buf.getvalue(), mimetype='image/png')
