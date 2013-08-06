# -*- coding: utf-8 -*-
import os
ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

ENV="Development"

SESSION_KEY_CAPTCHA = 'captcha_member'
SECRET_KEY = "adeaz%MemberSS(*U(*HD&$#"
LOGIN_SESSION_NAME = "adeazMemberLogin"

LOGIN_KEY = "7d26eda13b33c1257999de31bcd8ebfc"
REGISTER_KEY = "7a91bbcc7b447bdeb849193c1f805841"
SIG_KEY = "adeazMemberSigKey@#$%^&"

NEED_CHECK_ADMIN = ['/department','/position','/user']

USER_STATUS_OK = 0
USER_STATUS_DELETE = 1

class Config(object):
    HOST='0.0.0.0'
    PORT=8818
    DB_CONNECT_OPTIONS = {}

class ProductionConfig(Config):
    DEBUG=False

class DevelopmentConfig(Config):
    PORT=3888
    DEBUG=True
    DB_URI="mysql+oursql://root:@127.0.0.1/member?charset=utf8"
