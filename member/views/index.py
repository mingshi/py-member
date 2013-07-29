# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, url_for, redirect

mod = Blueprint("index", __name__)

@mod.route('/')
def index():
    username = request.cookies.get('m_username')
    if not username :
        return redirect("/login")
    else :
        return render_template("member/index.html",)
