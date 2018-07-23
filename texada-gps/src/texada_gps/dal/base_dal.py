'''
Created on Jul 20, 2018

@author: biya-bi
'''

from texada_gps.database import Database


class BaseDal:

    def __init__(self):
        self.db_session = None

    def find(self, search_criteria):
        pass
        
    def find_by_id(self, entity_id):
        pass
    
    def create(self, entity):
        self.validate(entity)
        session = self.get_db_session()
        session.add(entity)
        session.commit()

    def update(self, entity):
        self.validate(entity)
        session = self.get_db_session()
        session.merge(entity)
        session.commit()
        
    def delete(self, entity):
        session = self.get_db_session()
        session.delete(entity)
        session.commit()

    def get_db_session(self):
        if self.db_session is None:
            if Database.Session is None:
                Database.initialize()
            self.db_session = Database.Session()
        return self.db_session
    
    def validate(self,entity):
        pass