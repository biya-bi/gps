'''
Created on Jul 22, 2018

@author: biya-bi
'''
from texada_gps.exception.gps_exception import GpsException, \
    EntityNotFoundException


class LocationFieldRequiredException(GpsException):

    def __init__(self, message, field_name):
        super().__init__(message)
        self.field_name = field_name


class LocationNotFoundException(EntityNotFoundException):

    def __init__(self, location_id, message=None):
        if message is None:
            message = 'No location with id {} was found.'.format(location_id)
            
        super().__init__(message)
        
        self.location_id = location_id
