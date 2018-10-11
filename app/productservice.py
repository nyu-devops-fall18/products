from . import app
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_api import status    # HTTP Status Codes
from werkzeug.exceptions import NotFound
from app.productmodel import Product, ValidationError
from app.create_db import dbcreate

@app.route("/")
def index():
    app.logger.info(Product.query.all())
    return jsonify(name="Product Data API Service",
                   version='1.0', path=url_for("pricerange")), status.HTTP_200_OK

# LIST ALL FLOWERS
@app.route('/products', methods=['GET'])
def list_products():
     """ Return all the flowers"""
     flowers = []
     name = request.args.get('name')
     app.logger.info(name)
     category = request.args.get('category')
     if name:
         flowers = Product.find_by_name(name)
     elif category:
         flowers = Product.find_by_category(category)
     else:
         flowers = Product.all()

     results = [flower.serialize() for flower in flowers]
     return make_response(jsonify(results), status.HTTP_200_OK)


@app.route("/products/pricerange", methods=["GET"])
def pricerange():
    app.logger.info("Fetching products by provided price range")
    app.logger.info(request.args.get('minimum'))
    minimum = request.args.get('minimum')
    maximum = request.args.get('maximum')
    tlist = list(Product.search_by_price(minimum,maximum))
    result = []
    for i in tlist:
        result.append(i.serialize())
    app.logger.info(result)
    #result.append(i[0] for i in Product.search_by_price(minimum,maximum))
    #app.logger.info(result)
    return make_response(jsonify(result), status.HTTP_200_OK)

def initialize_logging(log_level=logging.INFO):
    """ Initialized the default logging to STDOUT """
    if not app.debug:
        print 'Setting up logging...'
        # Set up default logging for submodules to use STDOUT
        # datefmt='%m/%d/%Y %I:%M:%S %p'
        fmt = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        logging.basicConfig(stream=sys.stdout, level=log_level, format=fmt)
        # Make a new log handler that uses STDOUT
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(fmt))
        handler.setLevel(log_level)
        # Remove the Flask default handlers and use our own
        handler_list = list(app.logger.handlers)
        for log_handler in handler_list:
            app.logger.removeHandler(log_handler)
        app.logger.addHandler(handler)
        app.logger.setLevel(log_level)
        app.logger.info('Logging handler established')

def init_db():
    """ Initialies the SQLAlchemy app """
    global app
    Product.init_db(app)
