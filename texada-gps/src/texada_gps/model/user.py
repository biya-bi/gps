'''
Created on Jul 19, 2018

@author: biya-bi
'''

from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String

from texada_gps.model.base import Base


class User(Base):
    __tablename__ = 'user'
    
    id = Column('id', Integer, primary_key=True)
    username = Column('username', String(255), unique=True, nullable=False)
    password = Column('password', String(255), nullable=False)

    def __init__(self, username, password, user_id=None):
        self.id = user_id
        self.username = username
        self.password = password
        
    def __repr__(self):
        return '<User %r>' % self.username
