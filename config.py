# -*- coding: utf-8 -*-
import os
def hostname():  
    sys = os.name  
    if sys == 'nt':  
            hostname = os.getenv('computername')  
            return hostname  
    elif sys == 'posix':  
            host = os.popen('echo $HOSTNAME')  
            try:  
                    hostname = host.read()  
                    return hostname  
            finally:  
                    host.close()  
    else:  
            return 'Unkwon hostname' 


DEV_HOST = ['mingshi-hacking.local']

if hostname().strip('\n') in DEV_HOST :
    ENV = "Development"
else :
    ENV = "Production"


ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

SESSION_KEY_CAPTCHA = 'captcha_member'
SECRET_KEY = "adeaz%MemberSS(*U(*HD&$#"
LOGIN_SESSION_NAME = "adeazMemberLogin"

LOGIN_KEY = "7d26eda13b33c1257999de31bcd8ebfc"
REGISTER_KEY = "7a91bbcc7b447bdeb849193c1f805841"
SIG_KEY = "adeazMemberSigKey@#$%^&"

USER_INFO_KEY = "!adeazMemberUiFO7&^%"
USER_INFO_SIGN = "3ec8e544422a626075d904d0a9be0dcb"


NEED_CHECK_ADMIN = ['/department','/position','/user/add','/user/do_add']

USER_STATUS_OK = 0
USER_STATUS_DELETE = 1

class Config(object):
    HOST='0.0.0.0'
    PORT=8818
    DB_CONNECT_OPTIONS = {}

class ProductionConfig(Config):
    DEBUG=False
    DB_URI="mysql+oursql://root:pwd4root#@!@192.168.0.203:3307/member?charset=utf8"

class DevelopmentConfig(Config):
    PORT=3888
    DEBUG=True
    DB_URI="mysql+oursql://root:@127.0.0.1/member?charset=utf8"
