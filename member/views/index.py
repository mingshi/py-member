# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, url_for, redirect, session
from member import app

mod = Blueprint("index", __name__)

@mod.route('/')
def index():
    key = app.config['LOGIN_SESSION_NAME']
    if "'" + key + "'" in session :
        return render_template("member/index.html") 
    else :
        return redirect("/login")
