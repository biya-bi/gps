'''
Created on Jul 19, 2018

@author: biya-bi
'''
import os;
import sys

from flask import Flask, jsonify
from flask.globals import current_app
from flask.helpers import make_response
from flask_restful import abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker

from texada_gps.api.location_api import bp
from texada_gps.database import Database
from texada_gps.exception.gps_exception import FieldRequiredException, \
    EntityNotFoundException
from texada_gps.exception.location_dal_exception import LocationFieldRequiredException, \
    LocationNotFoundException
from texada_gps.exception.product_dal_exception import ProductFieldRequiredException, \
    ProductNotFoundException
from texada_gps.model.custom_json_encoder import CustomJsonEncoder
from texada_gps.security import auth


def create_app(test_config=None):
    app = Flask(__name__)
    # Set the JSON encoder
    app.json_encoder = CustomJsonEncoder
    
    app.config.from_mapping(
            SECRET_KEY='dev',
        )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)

    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    app.config['SQLALCHEMY_DATABASE_URI'] = Database.construct_db_url(os.path.join(app.instance_path, 'config.ini'))
    
    Database.Session = SQLAlchemy(app).session
    
    from texada_gps.api import product_api
    app.register_blueprint(product_api.bp)
    
    from texada_gps.api import location_api
    app.register_blueprint(location_api.bp)
    
    configure_gps_exception_handlers(app)
    configure_other_handlers(app)

    return app


def configure_gps_exception_handlers(app):   

    @app.errorhandler(LocationFieldRequiredException)
    @app.errorhandler(LocationNotFoundException)
    @app.errorhandler(ProductFieldRequiredException)
    @app.errorhandler(ProductNotFoundException)
    def handle(e): 
        app.logger.error(e)
        errorCode = None
        
        if  isinstance(e, LocationFieldRequiredException) or isinstance(e, ProductFieldRequiredException):
            errorCode = 400
        elif isinstance(e, LocationNotFoundException)or isinstance(e, ProductNotFoundException):
            errorCode = 404
        
        return make_response(jsonify({'errorMessage': str(e), 'errorCode':errorCode}), errorCode)


def configure_other_handlers(app):

    @app.errorhandler(400)
    def handle_bad_client_request(error):
        app.logger.error('Bad client request: %s', (error))
        return jsonify({'errorMessage': 'The was a bad client request.', 'errorCode':400}), 400
      
    @app.errorhandler(401)
    def handle_unauthorized_access(error):
        app.logger.error('Unauthorized access: %s', (error))
        return jsonify({'errorMessage': 'Unauthorized access.', 'errorCode':401}), 401
    
    @app.errorhandler(404)
    def handle_resource_not_found(error):
        app.logger.error('Resource not found: %s', (error))
        return jsonify({'errorMessage': 'A requested resource could not be found.', 'errorCode':404}), 404

    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        app.logger.error('Resource not found: %s', (error))
        return jsonify({'errorMessage': 'Method Not Allowed.', 'errorCode':405}), 405

    @app.errorhandler(500)
    def handle_internal_server_error(error):
        app.logger.error('Server Error: %s', (error))
        return jsonify({'errorMessage': 'An internal server error has occurred.', 'errorCode':500}), 500
    
    @app.errorhandler(Exception)
    def handle_unhandled_exception(e):
        # We log the exception before sending a response to the caller of the API
        app.logger.error('Server Error: %s', (e))
        return jsonify({'errorMessage': 'An unexpected error has occurred.', 'errorCode':500}), 500
