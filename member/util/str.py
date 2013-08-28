import re

def check_mobile(str) :
    return re.match(r"^1[3|4|5|8][0-9]\d{8}$", str)

def check_email(str) :
    return re.match(r"^(\w+([-+.]\w+)*)+@(\w)+((\.\w{2,3}){1,2})$", str)

def check_password(str) :
    return len(str) >= 8 and len(str) <= 20

def check_qq(str) :
    return re.match(r"^\d{5,10}$", str)
