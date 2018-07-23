'''
Created on Jul 22, 2018

@author: biya-bi
'''
from texada_gps.exception.gps_exception import GpsException, \
    EntityNotFoundException


class ProductFieldRequiredException(GpsException):

    def __init__(self, message, field_name):
        super().__init__(message)
        self.field_name = field_name


class ProductNotFoundException(EntityNotFoundException):

    def __init__(self, product_id, message=None):
        if message is None:
            message = 'No product with id {} was found.'.format(product_id)
            
        super().__init__(message)
        
        self.product_id = product_id
