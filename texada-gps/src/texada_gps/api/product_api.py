'''
Created on Jul 20, 2018

@author: biya-bi
'''
from flask import (
    Blueprint, request, jsonify, make_response
)

from texada_gps.dal.product_dal import ProductDal
from texada_gps.model.product import Product
from texada_gps.security import auth

bp = Blueprint('products', __name__, url_prefix='/texada_gps/api/products')


def is_int(s):
    try:
        int(s)
        return True
    except:
        return False

    
@bp.route('/', methods=('GET',))
def read():
    dal = ProductDal()
   
    page_number = request.args.get('page_number')
    page_size = request.args.get('page_size')
    
    if is_int(page_number):
        page_number = int(page_number)
    if is_int(page_size):
        page_size = int(page_size)
        
    products = dal.find(page_number=page_number, page_size=page_size)
    
    return jsonify(products)


@bp.route('/<int:product_id>', methods=('GET',))
def read_by_id(product_id):
    dal = ProductDal()  
    return jsonify(dal.find_by_id(product_id))


def _populate_from_request(product):
    if 'description' in request.json:
        product.description = request.json['description']
    else:
        product.description = None
    return product


@bp.route('/', methods=('POST',))
@auth.login_required
def create():
    product = _populate_from_request(Product())
    
    dal = ProductDal()
    dal.create(product)
    
    return make_response(jsonify(product), 201)


@bp.route('/<int:product_id>', methods=('PUT',))
@auth.login_required
def update(product_id):
    dal = ProductDal()  
    
    product = _populate_from_request(Product())
    product.id = product_id
    
    dal.update(product)
    
    return jsonify(product)


@bp.route('/<int:product_id>', methods=('DELETE',))
@auth.login_required
def delete(product_id):   
    dal = ProductDal()  
      
    dal.delete(dal.find_by_id(product_id))
    
    return jsonify({'result': True})
