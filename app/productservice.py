from . import app
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_api import status    # HTTP Status Codes
from werkzeug.exceptions import NotFound
from app.productmodel import Product, ValidationError

#########################
# error handlers
#########################
@app.errorhandler(ValidationError)
def request_validation_error(error):
    """ Handles Value Errors from bad data """
    return bad_request(error)

@app.errorhandler(400)
def bad_request(error):
    """ Handles bad reuests with 400_BAD_REQUEST """
    message = error.message or str(error)
    app.logger.info(message)
    return jsonify(status=400, error='Bad Request', message=message), 400

@app.errorhandler(404)
def not_found(error):
    """ Handles resources not found with 404_NOT_FOUND """
    message = error.message or str(error)
    app.logger.info(message)
    return jsonify(status=404, error='Not Found', message=message), 404

@app.errorhandler(405)
def method_not_supported(error):
    """ Handles unsuppoted HTTP methods with 405_METHOD_NOT_SUPPORTED """
    message = error.message or str(error)
    app.logger.info(message)
    return jsonify(status=405, error='Method not Allowed', message=message), 405

@app.errorhandler(415)
def mediatype_not_supported(error):
    """ Handles unsuppoted media requests with 415_UNSUPPORTED_MEDIA_TYPE """
    message = error.message or str(error)
    app.logger.info(message)
    return jsonify(status=415, error='Unsupported media type', message=message), 415

@app.errorhandler(500)
def internal_server_error(error):
    """ Handles unexpected server error with 500_SERVER_ERROR """
    message = error.message or str(error)
    app.logger.info(message)
    return jsonify(status=500, error='Internal Server Error', message=message), 500

@app.route("/")
def index():
    app.logger.info(Product.query.all())
    return jsonify(name="Product Data API Service",
                   version='1.0', path=url_for("pricerange")), status.HTTP_200_OK

#########################
# list all products
#########################
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

#########################
# list products by ID
#########################
@app.route('/products/<int:item_id>', methods=["GET"])
def list_products_by_id(item_id):
    app.logger.info('Finding a Product with id [{}]'.format(item_id))
    product = Product.find_by_id(item_id)
    if product:
        message = product.serialize()
        return_code = status.HTTP_200_OK
    else:
        message = {'error' : 'Product with id: %s was not found' % str(item_id)}
        return_code = status.HTTP_404_NOT_FOUND

    return jsonify(message), return_code

#########################
# list products by price range
#########################
@app.route("/products/pricerange", methods=["GET"])
def pricerange():
    app.logger.info("Fetching products by provided price range")
    # app.logger.info(request.args.get('minimum'))
    minimum = request.args.get('minimum')
    maximum = request.args.get('maximum')
    tlist = list(Product.search_by_price(minimum,maximum))
    result = []
    for i in tlist:
        result.append(i.serialize())
    # app.logger.info(result)
    return make_response(jsonify(result), status.HTTP_200_OK)

#########################
# update product by ID
#########################
@app.route("/products/<int:item_id>", methods=["PUT"])
def update_product(item_id):
    app.logger.info("Fetching the product")
    check_content_type("application/json")
    product = Product.find_by_id(item_id)
    # app.logger.info(product.rating)
    # prevrating = product.rating
    hitcount = product.updateCount
    if not product:
        raise NotFound("Product with id {} not found".format(item_id))
    # app.logger.info(product.deserialize(request.get_json()))
    product.deserialize(request.get_json())
    product.id = item_id
    # app.logger.info(product.rating)
    product.rating = product.totalrating/(hitcount+1)
    product.update()
    return make_response(jsonify(product.serialize()),status.HTTP_200_OK)

#########################
# delete product by ID
#########################
@app.route("/products/<int:item_id>", methods=["DELETE"])
def deleteproduct(item_id):
    app.logger.info("Deleting the product for the id provided")
    product = Product.find_by_id(item_id)
    if not product:
        raise NotFound("Product with id {} not found".format(item_id))
    product.delete()
    return make_response(" ", status.HTTP_204_NO_CONTENT)

def check_content_type(content_type):
    """ Checks that the media type is correct """
    app.logger.info(request.headers)
    if request.headers['Content-Type'] == content_type:
        return
    app.logger.error('Invalid Content-Type: %s', request.headers['Content-Type'])
    abort(415, 'Content-Type must be {}'.format(content_type))

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
