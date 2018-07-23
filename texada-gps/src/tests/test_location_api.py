'''
Created on Jul 19, 2018

@author: biya-bi
'''
import datetime
import json
import os

import pytest
from pytz import timezone

from tests.request_helper import get_authentication_header, execute_sql_script_files


@pytest.yield_fixture(autouse=True)
def setup_and_cleanup(app, db_engine):
    with app.app_context():

        execute_sql_script_files([os.path.join(os.path.dirname(__file__), 'clear_database.sql'),
                                  os.path.join(os.path.dirname(__file__), 'insert_users.sql'),
                                  os.path.join(os.path.dirname(__file__), 'insert_products.sql'),
                                  os.path.join(os.path.dirname(__file__), 'insert_locations.sql')], db_engine)
        yield
        
        execute_sql_script_files([os.path.join(os.path.dirname(__file__), 'clear_database.sql')], db_engine)

        
def test_read_all(client):
    response = client.get('/texada_gps/api/locations/')
  
    assert response.status_code == 200
    
    assert 17 == len(json.loads(response.data))


def test_read_pagination_from_page_number(client):
  
    response = client.get('/texada_gps/api/locations/?page_number=1&page_size=2')
  
    assert response.status_code == 200

    assert 2 == len(json.loads(response.data))


def test_read_pagination_from_second_page(client):
  
    response = client.get('/texada_gps/api/locations/?page_number=2&page_size=2')
  
    assert response.status_code == 200

    assert 2 == len(json.loads(response.data))


def test_read_by_id(client):
    location_id = 1
    
    response = client.get('/texada_gps/api/locations/{}'.format(location_id))
  
    assert response.status_code == 200
    
    expected_uri = 'http://localhost/texada_gps/api/locations/1'
    
    actual = json.loads(response.data)
      
    assert expected_uri == actual['uri']


def test_read_entity_not_found(client):
    location_id = 100000
    response = client.get('/texada_gps/api/locations/{}'.format(location_id))
  
    assert response.status_code == 404
    
    expected = {'errorMessage':'No location with id {} was found.'.format(location_id), 'errorCode':404}
    
    assert expected == json.loads(response.data)


# This method creates a product in a JSON format ready to be sent to the server
def _to_json(product_id, latitude, longitude, elevation, visit_date):
    return dict(product_id=product_id,
                      latitude=latitude,
                      longitude=longitude,
                      elevation=elevation,
                      visit_date=visit_date.__str__())

    
def _construct_new_location():
    return _to_json(product_id=1, latitude=85.0567, longitude=-92.54398, elevation=700, visit_date=datetime.datetime.utcnow())

          
# This test shows that if a user authenticates, then he/she can create a location.
def test_create(client):
    path = '/texada_gps/api/locations/'
    
    new_location = _construct_new_location()
      
    response = client.post(path,
                           data=json.dumps(new_location),
                           content_type='application/json', headers=get_authentication_header('admin', 'admin'))
                
    assert response.status_code == 201


# This test shows that if a user does not authenticate, then he/she cannot create a location.
def test_create_credentials_required(client):
    path = '/texada_gps/api/locations/'
 
    new_location = _construct_new_location()
      
    response = client.post(path,
                           data=json.dumps(new_location),
                           content_type='application/json')
                
    assert response.status_code == 401


# This test runs for each of the listed required fields
@pytest.mark.parametrize('required_field_name', (
    'product_id',
    'latitude',
    'longitude',
    'elevation',
    'visit_date',
))
def test_create_field_required(client, required_field_name):
    path = '/texada_gps/api/locations/'
 
    new_location = _construct_new_location()
    
    # We are deleting the required field from this JSON object so as to test that a
    # bad request error will occur if this field were omitted in the JSON object
    # sent to the server.
    del new_location[required_field_name]
    
    # No latitude has been included in the JSON sent to the server. Therefore, a bad request error will occur.
    response = client.post(path,
                           data=json.dumps(new_location),
                           content_type='application/json', headers=get_authentication_header('admin', 'admin'))
                
    assert response.status_code == 400
    
    expected = {'errorMessage': 'The {} field is required.'.format(required_field_name), 'errorCode':400}
    
    assert expected == json.loads(response.data) 
      

# This test shows that if a user authenticates, then he/she can update a location.
def test_update(client):
    location_id = 1
    
    path = '/texada_gps/api/locations/{}'.format(location_id)
    
    product_id = 1
    latitude = 90.52
    longitude = 86.75
    elevation = 550
    
    now = datetime.datetime.now()
    # We want to discard the part of the date after the microsecond to facilitate testing
    visit_date = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, now.second).astimezone(timezone('UTC'))

    location = _to_json(product_id=product_id, latitude=latitude, longitude=longitude, elevation=elevation, visit_date=visit_date)
    
    response = client.put(path,
                           data=json.dumps(location),
                           content_type='application/json', headers=get_authentication_header('admin', 'admin'))
                
    assert response.status_code == 200


# This test shows that if a user does not authenticate, then he/she cannot update a location.
def test_update_credentials_required(client):
    location_id = 1

    path = '/texada_gps/api/locations/{}'.format(location_id)
    
    product_id = 1
    latitude = 90.52
    longitude = 86.75
    elevation = 550
    
    visit_date = datetime.datetime.utcnow()
 
    location = _to_json(product_id=product_id, latitude=latitude, longitude=longitude, elevation=elevation, visit_date=visit_date)
    
    response = client.put(path,
                           data=json.dumps(location),
                           content_type='application/json')
    
    assert response.status_code == 401


def test_update_entity_not_found(client):
    location_id = 100000
    
    path = '/texada_gps/api/locations/{}'.format(location_id)
 
    product_id = 1
    latitude = 90.52
    longitude = 86.75
    elevation = 550
    
    visit_date = datetime.datetime.utcnow()
 
    location = _to_json(product_id=product_id, latitude=latitude, longitude=longitude, elevation=elevation, visit_date=visit_date)
    
    response = client.put(path,
                           data=json.dumps(location),
                           content_type='application/json', headers=get_authentication_header('admin', 'admin'))
  
    assert response.status_code == 404
    
    expected = {'errorMessage':'No location with id {} was found.'.format(location_id), 'errorCode':404}
    
    assert expected == json.loads(response.data)


# This test runs for each of the listed required fields
@pytest.mark.parametrize('required_field_name', (
    'product_id',
    'latitude',
    'longitude',
    'elevation',
    'visit_date',
))
def test_update_field_required(client, required_field_name):
    location_id = 1
    path = '/texada_gps/api/locations/{}'.format(location_id)

    product_id = 1
    latitude = 90.52
    longitude = 86.75
    elevation = 550 
    visit_date = datetime.datetime.utcnow()

    location = _to_json(product_id=product_id, latitude=latitude, longitude=longitude, elevation=elevation, visit_date=visit_date)
    
    # We are deleting the required field from this JSON object so as to test that a
    # bad request error will occur if this field were omitted in the JSON object
    # sent to the server.
    del location[required_field_name]
    
    response = client.put(path,
                           data=json.dumps(location),
                           content_type='application/json', headers=get_authentication_header('admin', 'admin'))
    
    expected = {'errorMessage': 'The {} field is required.'.format(required_field_name), 'errorCode':400}
    
    assert expected == json.loads(response.data)

 
# This test shows that if a user authenticates, then he/she can delete a location.
def test_delete(client):
    location_id = 1

    path = '/texada_gps/api/locations/{}'.format(location_id)

    response = client.delete(path,
                           content_type='application/json', headers=get_authentication_header('admin', 'admin'))
                
    assert response.status_code == 200
    assert json.loads(response.data) == {'result':True}


# This test shows that if a user does not authenticate, then he/she cannot delete a location.
def test_delete_credentials_required(client):
    location_id = 1

    path = '/texada_gps/api/locations/{}'.format(location_id)

    response = client.delete(path,
                           content_type='application/json')
                
    assert response.status_code == 401


def test_delete_entity_not_found(client):
    location_id = 100000
    
    path = '/texada_gps/api/locations/{}'.format(location_id)
 
    response = client.delete(path,
                           content_type='application/json', headers=get_authentication_header('admin', 'admin'))
  
    assert response.status_code == 404
    
    expected = {'errorMessage': 'No location with id {} was found.'.format(location_id), 'errorCode':404}
    
    assert expected == json.loads(response.data)


# This test shows that if an attempt is made to create a location with a non-existent product_id, a NOT_FOUND (404)
# error is occurs.
def test_create_product_not_found(client):
    path = '/texada_gps/api/locations/'
    
    non_existent_product_id = 10000
    
    new_location = _construct_new_location()
    new_location['product_id'] = non_existent_product_id
    
    response = client.post(path,
                           data=json.dumps(new_location),
                           content_type='application/json', headers=get_authentication_header('admin', 'admin'))
                
    assert response.status_code == 404
    
    expected = {'errorMessage': 'No product with id {} was found.'.format(non_existent_product_id), 'errorCode':404}
    
    assert expected == json.loads(response.data)


# This test shows that if an attempt is made to update a location with a non-existent product_id, a NOT_FOUND (404)
# error is occurs.
def test_update_product_not_found(client):
    location_id = 1
    
    path = '/texada_gps/api/locations/{}'.format(location_id)
    
    non_existent_product_id = 10000
    latitude = 90.52
    longitude = 86.75
    elevation = 550
    
    location = _to_json(product_id=non_existent_product_id, latitude=latitude, longitude=longitude, elevation=elevation, visit_date=datetime.datetime.utcnow())
    
    response = client.put(path,
                           data=json.dumps(location),
                           content_type='application/json', headers=get_authentication_header('admin', 'admin'))
                
    assert response.status_code == 404
    
    expected = {'errorMessage': 'No product with id {} was found.'.format(non_existent_product_id), 'errorCode':404}
    
    assert expected == json.loads(response.data)
