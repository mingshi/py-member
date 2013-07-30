# -*- coding: utf-8 -*-
import os
ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

ENV="Development"

SESSION_KEY_CAPTCHA = 'captcha_member'
SECRET_KEY = "adeaz%MemberSS(*U(*HD&$#"

class Config(object):
    HOST='0.0.0.0'
    PORT=8818
    DB_CONNECT_OPTIONS = {}

class ProductionConfig(Config):
    DEBUG=False

class DevelopmentConfig(Config):
    PORT=3888
    DEBUG=True
    DB_URI="mysql+oursql://root:@127.0.0.1/member"
