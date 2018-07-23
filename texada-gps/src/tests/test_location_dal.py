'''
Created on Jul 22, 2018

@author: biya-bi
'''

import datetime
import os

from pytest import raises
import pytest

from tests.request_helper import execute_sql_script_files
from texada_gps.dal.location_dal import LocationDal
from texada_gps.exception.location_dal_exception import LocationFieldRequiredException, \
    LocationNotFoundException
from texada_gps.model.location import Location


@pytest.yield_fixture(autouse=True)
def setup_and_cleanup(app, db_engine):
    with app.app_context():

        execute_sql_script_files([os.path.join(os.path.dirname(__file__), 'clear_database.sql'),
                                  os.path.join(os.path.dirname(__file__), 'insert_products.sql'),
                                  os.path.join(os.path.dirname(__file__), 'insert_locations.sql')], db_engine)
        yield
        
        execute_sql_script_files([os.path.join(os.path.dirname(__file__), 'clear_database.sql')], db_engine)


def test_create():
        dal = LocationDal()
        expected = Location(product_id=1, latitude=-85, longitude=94, elevation=600, visit_date=datetime.datetime.utcnow())
        assert expected.id is None
        
        dal.create(expected)
        
        assert expected.id is not None
        
        actual = dal.find_by_id(expected.id)
        
        assert expected.id == actual.id
        assert expected.product_id == actual.product_id
        assert expected.latitude == actual.latitude
        assert expected.longitude == actual.longitude
        assert expected.elevation == actual.elevation


def test_create_product_id_required():
    location = Location(latitude=-85, longitude=94, elevation=600, visit_date=datetime.datetime.utcnow())
    with raises(LocationFieldRequiredException):
        try:
            dal = LocationDal()
            dal.create(location)
        except LocationFieldRequiredException as e:
            assert e.field_name == 'product_id'
            assert str(e) == 'The product_id field is required.'
            raise


def test_create_latitude_required():
    location = Location(product_id=1, longitude=94, elevation=600, visit_date=datetime.datetime.utcnow())
    with raises(LocationFieldRequiredException):
        try:
            dal = LocationDal()
            dal.create(location)
        except LocationFieldRequiredException as e:
            assert e.field_name == 'latitude'
            assert str(e) == 'The latitude field is required.'
            raise


def test_create_longitude_required():
    location = Location(product_id=1, latitude=-85, elevation=600, visit_date=datetime.datetime.utcnow())
    with raises(LocationFieldRequiredException):
        try:
            dal = LocationDal()
            dal.create(location)
        except LocationFieldRequiredException as e:
            assert e.field_name == 'longitude'
            assert str(e) == 'The longitude field is required.'
            raise


def test_create_elevation_required():
    location = Location(product_id=1, latitude=-85, longitude=94, visit_date=datetime.datetime.utcnow())
    with raises(LocationFieldRequiredException):
        try:
            dal = LocationDal()
            dal.create(location)
        except LocationFieldRequiredException as e:
            assert e.field_name == 'elevation'
            assert str(e) == 'The elevation field is required.'
            raise

        
def test_create_visit_date_required():
    location = Location(product_id=1, latitude=-85, longitude=94, elevation=600)
    with raises(LocationFieldRequiredException):
        try:
            dal = LocationDal()
            dal.create(location)
        except LocationFieldRequiredException as e:
            assert e.field_name == 'visit_date'
            assert str(e) == 'The visit_date field is required.'
            raise
                    

def test_update():
        dal = LocationDal()
        
        location_id = 1
         
        expected = Location(location_id=location_id, product_id=1, latitude=-85, longitude=94, elevation=600, visit_date=datetime.datetime.utcnow())
       
        dal.update(expected)
        
        actual = dal.find_by_id(location_id)
        
        assert expected.id == actual.id
        assert expected.product_id == actual.product_id
        assert expected.latitude == actual.latitude
        assert expected.longitude == actual.longitude
        assert expected.elevation == actual.elevation


def test_update_product_id_required():
    location = Location(location_id=1, latitude=-85, longitude=94, elevation=600, visit_date=datetime.datetime.utcnow())
    with raises(LocationFieldRequiredException):
        try:
            dal = LocationDal()
            dal.update(location)
        except LocationFieldRequiredException as e:
            assert e.field_name == 'product_id'
            assert str(e) == 'The product_id field is required.'
            raise


def test_update_latitude_required():
    location = Location(location_id=1, product_id=1, longitude=94, elevation=600, visit_date=datetime.datetime.utcnow())
    with raises(LocationFieldRequiredException):
        try:
            dal = LocationDal()
            dal.update(location)
        except LocationFieldRequiredException as e:
            assert e.field_name == 'latitude'
            assert str(e) == 'The latitude field is required.'
            raise


def test_update_longitude_required():
    location = Location(location_id=1, product_id=1, latitude=-85, elevation=600, visit_date=datetime.datetime.utcnow())
    with raises(LocationFieldRequiredException):
        try:
            dal = LocationDal()
            dal.update(location)
        except LocationFieldRequiredException as e:
            assert e.field_name == 'longitude'
            assert str(e) == 'The longitude field is required.'
            raise


def test_update_elevation_required():
    location = Location(location_id=1, product_id=1, latitude=-85, longitude=94, visit_date=datetime.datetime.utcnow())
    with raises(LocationFieldRequiredException):
        try:
            dal = LocationDal()
            dal.update(location)
        except LocationFieldRequiredException as e:
            assert e.field_name == 'elevation'
            assert str(e) == 'The elevation field is required.'
            raise

        
def test_update_visit_date_required():
    location = Location(location_id=1, product_id=1, latitude=-85, longitude=94, elevation=600)
    with raises(LocationFieldRequiredException):
        try:
            dal = LocationDal()
            dal.update(location)
        except LocationFieldRequiredException as e:
            assert e.field_name == 'visit_date'
            assert str(e) == 'The visit_date field is required.'
            raise


def test_find_by_id():
    with raises(LocationNotFoundException):
        location_id = 10000000
        try:
            dal = LocationDal()
            dal.find_by_id(location_id)
        except LocationNotFoundException as e:
            assert e.location_id == location_id
            assert str(e) == 'No location with id {} was found.'.format(location_id)
            raise

