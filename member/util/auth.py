# -*- coding: utf-8 -*-

from flask import Flask, session, redirect

def check_admin() :
    if ('member_is_admin' in session) and (session['member_is_admin'] == 1) :
        return "1"
    else :
        return None

