'''
Created on Jul 16, 2018

@author: biya-bi
'''
from texada_gps import create_app


def test_config():
    assert not create_app().testing
    assert create_app({
        'TESTING': True,
        'DB_USER':'root',
        'DB_PASSWORD':'Passw0rd',
        'DB_NAME':'flaskr_tests',
        'DB_HOST':'localhost',
        'DB_PORT':'3306',
        'DB_URL_FORMAT':'mysql+pymysql://{}:{}@{}:{}/{}',
        'SQLALCHEMY_TRACK_MODIFICATIONS':'False'
    }).testing