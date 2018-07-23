'''
Created on Jul 22, 2018

@author: biya-bi
'''

import configparser

from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker


class Database:
    engine = None
    Session = None

    @staticmethod
    def initialize(db_url):
        engine = create_engine(db_url)  
        Database.engine = engine
        Database.Session = sessionmaker(bind=engine)
    
    @staticmethod
    def construct_db_url(path):
        config = configparser.ConfigParser()
        
        config.read(path)
        
        section = config['DATABASE']
        
        return section['DB_URL_FORMAT'].format(section['DB_USER'], section['DB_PASSWORD'], section['DB_HOST'],
                                                                             section['DB_PORT'],
                                                                          section['DB_NAME'])