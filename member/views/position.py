# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, redirect, url_for, request, session
from member.util.auth import *

mod = Blueprint("position", __name__)

@mod.route('/position')
def position() :
    if check_admin() :
        return "111"
    else :
        return redirect('/403')
