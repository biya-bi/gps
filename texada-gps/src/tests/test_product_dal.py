'''
Created on Jul 22, 2018

@author: biya-bi
'''
import os

from pytest import raises
import pytest

from tests.request_helper import execute_sql_script_files
from texada_gps.dal.product_dal import ProductDal
from texada_gps.exception.product_dal_exception import ProductFieldRequiredException, \
    ProductNotFoundException
from texada_gps.model.product import Product


@pytest.yield_fixture(autouse=True)
def setup_and_cleanup(app, db_engine):
    with app.app_context():

        execute_sql_script_files([os.path.join(os.path.dirname(__file__), 'clear_database.sql'),
                                  os.path.join(os.path.dirname(__file__), 'insert_products.sql')], db_engine)
        yield
        
        execute_sql_script_files([os.path.join(os.path.dirname(__file__), 'clear_database.sql')], db_engine)


def test_create():
        dal = ProductDal()
        expected = Product(description='Hubble Satellite')
        assert expected.id is None
        
        dal.create(expected)
        
        assert expected.id is not None
        
        actual = dal.find_by_id(expected.id)
        
        assert expected.id == actual.id
        assert expected.description == actual.description


def test_create_description_required():
    with raises(ProductFieldRequiredException):
        try:
            dal = ProductDal()
            dal.create(Product())
        except ProductFieldRequiredException as e:
            assert e.field_name == 'description'
            assert str(e) == 'The description field is required.'
            raise


def test_update():
        dal = ProductDal()
        product_id = 1
        expected = Product(product_id=product_id, description='Hubble Satellite')
       
        dal.update(expected)
        
        actual = dal.find_by_id(product_id)
        
        assert expected.description == actual.description


def test_update_description_required():
    with raises(ProductFieldRequiredException):
        try:
            dal = ProductDal()
            product = dal.find_by_id(1)
            product.description = ''
            dal.update(product)
        except ProductFieldRequiredException as e:
            assert e.field_name == 'description'
            assert str(e) == 'The description field is required.'
            raise


def test_find_by_id():
    with raises(ProductNotFoundException):
        product_id = 10000000
        try:
            dal = ProductDal()
            dal.find_by_id(product_id)
        except ProductNotFoundException as e:
            assert e.product_id == product_id
            assert str(e) == 'No product with id {} was found.'.format(product_id)
            raise
