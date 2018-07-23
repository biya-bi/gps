'''
Created on Jul 20, 2018

@author: biya-bi
'''

from sqlalchemy.sql.expression import asc

from texada_gps.dal.base_dal import BaseDal
from texada_gps.exception.product_dal_exception import ProductNotFoundException, \
    ProductFieldRequiredException
from texada_gps.model.product import Product


class ProductDal(BaseDal):

    def find_by_description(self, description):
        return self.get_db_session().query(Product).filter(Product.description == description).first()

    def find_by_id(self, entity_id):
        product = self.get_db_session().query(Product).filter(Product.id == entity_id).first()
        if product is None:
            raise ProductNotFoundException(entity_id)
        return product
    
    def find(self, page_number=None, page_size=None):
        
        query = self.get_db_session().query(Product).order_by(asc(Product.description))
 
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
        if not entity.description:
            field_name = 'description'
            raise ProductFieldRequiredException(message='The {} field is required.'.format(field_name), field_name=field_name)
        
        # The below condition will raise a ProductNotFoundException if the product id is not None and the corresponding product does not exist.
        if entity.id:
            self.find_by_id(entity.id)
    
