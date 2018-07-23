'''
Created on Jul 20, 2018

@author: biya-bi
'''
from texada_gps.model.user import User
from texada_gps.dal.base_dal import BaseDal


class UserDal(BaseDal):

    def find_by_username(self, username):
        return self.get_db_session().query(User).filter(User.username == username).first()

    def find_by_id(self, entity_id):
        return self.get_db_session().query(User).filter(User.id == entity_id).first()
            
