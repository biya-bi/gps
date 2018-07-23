'''
Created on Jul 20, 2018

@author: biya-bi
'''
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String

from texada_gps.model.base import Base

class Product(Base):
    __tablename__ = 'product'
    
    id = Column('id', Integer, primary_key=True)
    description = Column('description', String(255), unique=True, nullable=False)

    def __init__(self, description=None, product_id=None):
        self.description = description
        self.id = product_id
        
    def __repr__(self):
        return '<Product %r>' % self.description
