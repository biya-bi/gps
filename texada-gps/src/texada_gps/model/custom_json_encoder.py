'''
Created on Jul 20, 2018

@author: biya-bi
'''
from flask import url_for
from flask.json import JSONEncoder


class CustomJsonEncoder(JSONEncoder):

    def default(self, obj):
        from texada_gps.model.product import Product
        from texada_gps.model.location import Location
        
        if isinstance(obj, Product):
            return {
            'description':obj.description,
            'uri' : url_for('products.read_by_id', product_id=obj.id, _external=True)
            }
            
        if isinstance(obj, Location):
            return {
            'uri' : url_for('locations.read_by_id', location_id=obj.id, _external=True),
            'product':url_for('products.read_by_id', product_id=obj.product_id, _external=True),
            'latitude':obj.latitude,
            'longitude':obj.longitude,
            'elevation':obj.elevation,
            'visit_date':obj.visit_date.isoformat(),
            }
        return JSONEncoder.default(self, obj)

