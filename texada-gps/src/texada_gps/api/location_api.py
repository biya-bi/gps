'''
Created on Jul 19, 2018

@author: biya-bi
'''
from dateutil import parser
from flask import (
    Blueprint, request, jsonify, make_response
)
from pytz import timezone

from texada_gps.dal.location_dal import LocationDal
from texada_gps.model.location import Location
from texada_gps.security import auth

bp = Blueprint('locations', __name__, url_prefix='/texada_gps/api/locations')


def _populate_from_request(location):

    if 'product_id' in request.json:
        location.product_id = request.json['product_id']
    else:
        location.product_id = None
        
    if 'latitude' in request.json:
        location.latitude = request.json['latitude']
    else:
        location.latitude = None
        
    if 'longitude' in request.json:
        location.longitude = request.json['longitude']
    else:
        location.longitude = None
        
    if 'elevation' in request.json:
        location.elevation = request.json['elevation']
    else:
        location.elevation = None
        
    if 'visit_date' in request.json:
        location.visit_date = parser.parse(request.json['visit_date']).astimezone(timezone('UTC'))
    else:
        location.visit_date = None
        
    return location


def is_int(s):
    try:
        int(s)
        return True
    except:
        return False

    
@bp.route('/', methods=('GET',))
def read():
    dal = LocationDal()
   
    page_number = request.args.get('page_number')
    page_size = request.args.get('page_size')
    
    if is_int(page_number):
        page_number = int(page_number)
    if is_int(page_size):
        page_size = int(page_size)
        
    locations = dal.find(page_number=page_number, page_size=page_size)
    
    return jsonify(locations)


@bp.route('/<int:location_id>', methods=('GET',))
def read_by_id(location_id):
    dal = LocationDal()

    return jsonify(dal.find_by_id(location_id))

 
@bp.route('/', methods=('POST',))
@auth.login_required
def create():
    location = _populate_from_request(Location())
    
    dal = LocationDal()
    dal.create(location)
    
    return make_response(jsonify(location), 201)

@bp.route('/<int:location_id>', methods=('PUT',))
@auth.login_required
def update(location_id):
    dal = LocationDal()  

    location = _populate_from_request(Location())
    location.id = location_id
    
    dal.update(location)
    
    return jsonify(location)


@bp.route('/<int:location_id>', methods=('DELETE',))
@auth.login_required
def delete(location_id):   
    dal = LocationDal()  
    
    dal.delete(dal.find_by_id(location_id))
    
    return jsonify({'result': True})
    
