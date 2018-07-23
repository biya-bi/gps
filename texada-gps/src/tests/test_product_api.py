'''
Created on Jul 19, 2018

@author: biya-bi
'''
import json
import os

import pytest

from tests.request_helper import get_authentication_header, execute_sql_script_files


@pytest.yield_fixture(autouse=True)
def setup_and_cleanup(app, db_engine):
    with app.app_context():

        execute_sql_script_files([os.path.join(os.path.dirname(__file__), 'clear_database.sql'),
                                  os.path.join(os.path.dirname(__file__), 'insert_users.sql'),
                                  os.path.join(os.path.dirname(__file__), 'insert_products.sql')], db_engine)
        yield
        
        execute_sql_script_files([os.path.join(os.path.dirname(__file__), 'clear_database.sql')], db_engine)


def test_read_all(client):
    response = client.get('/texada_gps/api/products/')
  
    assert response.status_code == 200

    expected = [
          {
            'description': 'Art Boom 6500',
            'uri': 'http://localhost/texada_gps/api/products/4'
          },
          {
            'description': 'Cesna 120',
            'uri': 'http://localhost/texada_gps/api/products/1'
          },
          {
            'description': 'DC-6 Twin Otter',
            'uri': 'http://localhost/texada_gps/api/products/2'
          },
          {
            'description': 'Piper M600',
            'uri': 'http://localhost/texada_gps/api/products/3'
          }
        ]
    
    assert expected == json.loads(response.data)


def test_read_pagination_from_page_number(client):
  
    response = client.get('/texada_gps/api/products/?page_number=1&page_size=2')
  
    assert response.status_code == 200

    expected = [
          {
            'description': 'Art Boom 6500',
            'uri': 'http://localhost/texada_gps/api/products/4'
          },
          {
            'description': 'Cesna 120',
            'uri': 'http://localhost/texada_gps/api/products/1'
          },
        ]
    
    assert expected == json.loads(response.data)


def test_read_pagination_from_second_page(client):
  
    response = client.get('/texada_gps/api/products/?page_number=2&page_size=2')
  
    assert response.status_code == 200

    expected = [
          {
            'description': 'DC-6 Twin Otter',
            'uri': 'http://localhost/texada_gps/api/products/2'
          },
          {
            'description': 'Piper M600',
            'uri': 'http://localhost/texada_gps/api/products/3'
          }
        ]
    
    assert expected == json.loads(response.data)

    
def test_read_by_id(client):
    product_id = 1
    
    url = 'http://localhost/texada_gps/api/products/{}'.format(product_id)
    
    response = client.get(url)
  
    assert response.status_code == 200
    
    expected = {'description': 'Cesna 120', 'uri': url }
    
    assert expected == json.loads(response.data)


def test_read_entity_not_found(client):
    product_id = 100000
    response = client.get('/texada_gps/api/products/{}'.format(product_id))
  
    assert response.status_code == 404
    
    expected = {'errorMessage': 'No product with id {} was found.'.format(product_id), 'errorCode':404}
    
    assert expected == json.loads(response.data)

    
# This test shows that if a user authenticates, then he/she can create a product.
def test_create(client):
    path = '/texada_gps/api/products/'
 
    response = client.post(path,
                           data=json.dumps(dict(description='Hubble Space Telescope')),
                           content_type='application/json', headers=get_authentication_header('admin', 'admin'))
              
    assert response.status_code == 201
    

# This test shows that if a user does not authenticate, then he/she cannot create a product.
def test_create_credentials_required(client):
    path = '/texada_gps/api/products/'
 
    response = client.post(path,
                           data=json.dumps(dict(description='Galaxy 14')),
                           content_type='application/json')
                
    assert response.status_code == 401


def test_create_description_required(client):
    path = '/texada_gps/api/products/'
 
    # No description has been included in the JSON sent to the server. Therefore, a bad request error will occur.
    response = client.post(path,
                           data=json.dumps(dict({'sample_field_name':'sample_field_value'})),
                           content_type='application/json', headers=get_authentication_header('admin', 'admin'))
                
    assert response.status_code == 400
    
    expected = {'errorMessage': 'The description field is required.', 'errorCode':400}
    
    assert expected == json.loads(response.data) 


# This test shows that if a user authenticates, then he/she can update a product.
def test_update(client):
    product_id = 1
    
    path = '/texada_gps/api/products/{}'.format(product_id)
 
    description = 'GOES-12'
    
    response = client.put(path,
                           data=json.dumps(dict(description=description)),
                           content_type='application/json', headers=get_authentication_header('admin', 'admin'))
                
    assert response.status_code == 200


# This test shows that if a user does not authenticate, then he/she cannot update a product.
def test_update_credentials_required(client):
    product_id = 1
    
    path = '/texada_gps/api/products/{}'.format(product_id)
 
    new_description = 'GOES-12'
    
    response = client.put(path,
                           data=json.dumps(dict(description=new_description)),
                           content_type='application/json')
                
    assert response.status_code == 401


def test_update_entity_not_found(client):
    product_id = 100000
    
    path = '/texada_gps/api/products/{}'.format(product_id)
 
    description = 'GOES-12'
    
    response = client.put(path,
                           data=json.dumps(dict(description=description)),
                           content_type='application/json', headers=get_authentication_header('admin', 'admin'))
  
    assert response.status_code == 404
    
    expected = {'errorMessage': 'No product with id {} was found.'.format(product_id), 'errorCode':404}
    
    assert expected == json.loads(response.data)


def test_update_description_required(client):
    product_id = 1
    path = '/texada_gps/api/products/{}'.format(product_id)
 
    # No description has been included in the JSON sent to the server. Therefore, a bad request error will occur.
    response = client.put(path,
                           data=json.dumps(dict({'sample_field_name':'sample_field_value'})),
                           content_type='application/json', headers=get_authentication_header('admin', 'admin'))
                
    assert response.status_code == 400
    
    expected = {'errorMessage': 'The description field is required.', 'errorCode':400}
    
    assert expected == json.loads(response.data) 

        
# This test shows that if a user authenticates, then he/she can delete a product.
def test_delete(client):
    product_id = 1
    
    path = '/texada_gps/api/products/{}'.format(product_id)

    response = client.delete(path,
                           content_type='application/json', headers=get_authentication_header('admin', 'admin'))
                
    assert response.status_code == 200
    assert json.loads(response.data) == {'result':True}
   
    
# This test shows that if a user does not authenticate, then he/she cannot delete a product.
def test_delete_credentials_required(client):
    product_id = 1

    path = '/texada_gps/api/products/{}'.format(product_id)

    response = client.delete(path,
                           content_type='application/json')
                
    assert response.status_code == 401 


def test_delete_entity_not_found(client):
    product_id = 100000
    
    path = '/texada_gps/api/products/{}'.format(product_id)
 
    response = client.delete(path,
                           content_type='application/json', headers=get_authentication_header('admin', 'admin'))
  
    assert response.status_code == 404
    
    expected = {'errorMessage': 'No product with id {} was found.'.format(product_id), 'errorCode':404}
    
    assert expected == json.loads(response.data)
