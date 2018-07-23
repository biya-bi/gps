'''
Created on Jul 20, 2018

@author: biya-bi
'''
from sqlalchemy.sql.expression import asc

from texada_gps.dal.base_dal import BaseDal
from texada_gps.dal.product_dal import ProductDal
from texada_gps.exception.location_dal_exception import LocationNotFoundException, \
    LocationFieldRequiredException
from texada_gps.model.location import Location


class LocationDal(BaseDal):

    def find_by_id(self, entity_id):
        location = self.get_db_session().query(Location).filter(Location.id == entity_id).first()
        if location is None:
            raise LocationNotFoundException(entity_id)
        return location
    
    def find(self, page_number=None, page_size=None):
        
        query = self.get_db_session().query(Location).order_by(asc(Location.id))
 
        if (page_number is not None) and (page_size is not None):
            return query.paginate(page_number, page_size, False).items
        if (page_size is not None):
            # If we enter here, we are sure that page_number is None. Therefore,
            # from the first page we read page_size number of rows.
            return query.paginate(1, page_size, False).items
        # If we reach this point, then the page_size is None. In this case, no matter the
        # value of page_number, we read all the rows.
        return query.all()
    
   
    def validate(self, entity):
        required_field_message_template = 'The {} field is required.'
        required_field_name = None
        
        if not entity.product_id:
            required_field_name = 'product_id'
        elif not entity.latitude:
            required_field_name = 'latitude'
        elif not entity.longitude:
            required_field_name = 'longitude'
        elif not entity.elevation:
            required_field_name = 'elevation'
        elif not entity.visit_date:
            required_field_name = 'visit_date'
              
        if required_field_name:
            raise LocationFieldRequiredException(message=required_field_message_template.format(required_field_name), field_name=required_field_name)
        
        # The below condition will raise a LocationNotFoundException if the location id is not None and the corresponding location does not exist.
        if entity.id:
            self.find_by_id(entity.id)
            
        # If the product is not found, the below line will raise a ProductNotFoundException
        ProductDal().find_by_id(entity.product_id)
        
        