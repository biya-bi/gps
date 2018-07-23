'''
Created on Jul 22, 2018

@author: biya-bi
'''
class GpsException(Exception):
    def __init__(self,message):
        super().__init__(message)
        
class EntityNotFoundException(GpsException):
    pass

class FieldRequiredException(GpsException):

    def __init__(self, message, field_name):
        super().__init__(message)
        self.field_name = field_name