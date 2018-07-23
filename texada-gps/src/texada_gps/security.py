'''
Created on Jul 21, 2018

@author: biya-bi
'''
from flask_httpauth import HTTPBasicAuth
from flask_restful import abort
from werkzeug.security import check_password_hash


auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    from texada_gps.dal.user_dal import UserDal
    user = UserDal().find_by_username(username)
    if user is None or (not check_password_hash(user.password, password)):
        return False
    return True

@auth.error_handler
def unauthorized():
    return abort(401)
