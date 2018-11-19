from . import app
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_api import status    # HTTP Status Codes
from werkzeug.exceptions import NotFound
from app.model import Product, ValidationError

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

#########################
# Index Page
#########################
@app.route("/")
def index():
    app.logger.info(Product.query.all())
    # return jsonify(name="Product Demo REST API Service",
    #                version='1.0', Get_All_Products="[GET] /products",
    #                Get_Latest_Products="[GET] /products/latest",
    #                Get_Product_By_ID="[GET] /products?id=<item_id>",
    #                Get_Product_By_Category="[GET] /products?category=<category>",
    #                Get_Product_By_Name="[GET] /products?name=<name>",
    #                Get_Product_By_PriceRange="[GET] /products/pricerange?minimum=<min-price>&maximum=<max_price>",
    #                Create_Product="[POST] /products/",
    #                Update_Product="[PUT] /products/<item_id>",
    #                Update_Product_Rating="[PUT] /products/rating/<item_id>?stars=<rating from [1,10]>",
    #                Delete_Product="[DELETE] /products/<item_id>",
    #                Delete_All_Products="[DELETE] /products"
    #                ), status.HTTP_200_OK
    #Please comment above return statement and uncommment the below return statement FOR BEHAVIORAL TESTING
    return app.send_static_file('index.html')
#########################
# list all products
#########################
@app.route('/products', methods=['GET'])
def list_products():
     """ Return all the products"""
     products = []
     name = request.args.get('name')
     app.logger.info(name)
     category = request.args.get('category')
     if name:
         products = Product.find_by_name(name)
     elif category:
         products = Product.find_by_category(category)
     else:
         products = Product.all()

     results = [product.serialize() for product in products]
     return make_response(jsonify(results), status.HTTP_200_OK)


#########################
# Sort products by date
#########################
@app.route('/products/latest', methods=['GET'])
def sort_by_date():
    """List all the product by their updated date"""
    app.logger.info("List products by updated date")
    sorted_products = Product.sort_by_date()
    results = [ product.serialize() for product in sorted_products]
    return make_response(jsonify(results), status.HTTP_200_OK)


#########################
# create a product
#########################
@app.route('/products', methods=['POST'])
def create_products():
    """
    Creates a Pet
    This endpoint will create a Pet based the data in the body that is posted
    """
    check_content_type('application/json')
    product = Product(1,"","","",0,"",0,"",0)
    product.deserialize(request.get_json())
    product.save()
    message = product.serialize()
    location_url = url_for('list_products_by_id', item_id=product.id, _external=True)
    return make_response(jsonify(message), status.HTTP_201_CREATED,
                         {
                             'Location': location_url
                         })

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
        raise NotFound(message)
        # return_code = status.HTTP_404_NOT_FOUND

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
    if not product:
        raise NotFound("Product with id {} not found".format(item_id))
    # app.logger.info(product.deserialize(request.get_json()))
    hitcount = product.updateCount
    product.deserialize(request.get_json())
    product.id = item_id
    # app.logger.info(product.rating)
    product.rating = product.totalrating/(hitcount+1)
    product.update()
    return make_response(jsonify(product.serialize()),status.HTTP_200_OK)

#############################
# update product rating by ID
#############################
@app.route("/products/rating/<int:item_id>", methods=["PUT"])
def update_product_rating(item_id):
    app.logger.info("Fetching the product")
    check_content_type("application/json")
    product = Product.find_by_id(item_id)
    hitcount = product.updateCount
    newrating = request.args.get('stars')
    print(newrating)
    if not product:
        raise NotFound("Product with id {} not found".format(item_id))
    # app.logger.info(product.deserialize(request.get_json()))
    # product.deserialize(request.get_json())
    # product.id = item_id
    # app.logger.info(product.rating)
    product.rating = (int(product.totalrating) + int(newrating))/(hitcount+1)
    product.update()
    return make_response(jsonify(product.serialize()),status.HTTP_200_OK)

#############################
# update product review by ID
#############################
@app.route("/products/review/<int:item_id>", methods=["PUT"])
def update_product_review(item_id):
    app.logger.info("Fetching the product")
    check_content_type("application/json")
    product = Product.find_by_id(item_id)
    newreview = request.args.get('newrev')
    print(newreview)
    if not product:
        raise NotFound("Product with id {} not found".format(item_id))
    if not product.review:
         product.review = str(newreview)
    else:
        product.review = str(product.review) + "|" + str(newreview)
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
        return make_response("Product does not exist", status.HTTP_204_NO_CONTENT)
    product.delete()
    return make_response(" ", status.HTTP_204_NO_CONTENT)

#########################
# delete all products
#########################
@app.route("/products", methods=["DELETE"])
def deleteallproducts():
    app.logger.info("Deleting all products")
    Product.delete_all()
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
