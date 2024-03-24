from flask import current_app
import platform
import re

def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email))

def get_os():
    os_name = platform.system()
    if os_name == 'Windows':
        return 'Windows'
    elif os_name == 'Linux':
        return 'Linux'
    else:
        return 'Unknown'
def getIp():
    if get_os() == 'Windows':
        return 'localhost'
    elif get_os() == 'Linux':
        #return '192.168.0.1'
        return '172.17.0.1' 

    