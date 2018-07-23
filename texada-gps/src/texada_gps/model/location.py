'''
Created on Jul 20, 2018

@author: biya-bi
'''
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, Float, TIMESTAMP

from texada_gps.model.base import Base
from sqlalchemy.orm import relationship


class Location(Base):
    __tablename__ = 'location'
    
    id = Column('id', Integer, primary_key=True)
    product_id = Column(ForeignKey('product.id'), nullable=False)
    latitude = Column('latitude', Float, nullable=False)
    longitude = Column('longitude', Float, nullable=False)
    elevation = Column('elevation', Integer, nullable=False)
    visit_date = Column('visit_date', TIMESTAMP, nullable=False)
    
    from texada_gps.model.product import Product
    product = relationship(Product, lazy="joined", innerjoin=True)
    
    def __init__(self, product_id=None, latitude=None, longitude=None, elevation=None, visit_date=None, location_id=None):
        self.product_id = product_id
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation
        self.visit_date = visit_date
        self.id = location_id
