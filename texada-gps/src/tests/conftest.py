'''
Created on Jul 16, 2018

@author: biya-bi
'''
import os

import pytest
from sqlalchemy import create_engine

from tests.request_helper import  execute_sql_script_files
from texada_gps import create_app
from texada_gps.database import Database


@pytest.fixture(scope="session")
def initialize_database():
    Database.initialize(Database.construct_db_url(os.path.join(app.instance_path, 'config.ini')))

    
@pytest.fixture(scope="session")
def db_engine(app):
    return create_engine(app.config['SQLALCHEMY_DATABASE_URI']);


@pytest.fixture(scope="session")
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_TRACK_MODIFICATIONS':'False'
    })

    with app.app_context():
        engine = db_engine(app)
        
        execute_sql_script_files([os.path.join(os.path.dirname(__file__), 'clear_database.sql'),
                                  os.path.join(os.path.dirname(__file__), 'reset_auto_increment.sql')], engine)
    
        yield app

        engine.dispose()

 
@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
    

class AuthActions(object):

    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)

