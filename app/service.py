from . import app
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_api import status    # HTTP Status Codes
from werkzeug.exceptions import NotFound
from app.model import Product, ValidationError
from flask_restplus import Api, Resource, fields, reqparse, abort

######################################################################
# Configure Swagger before initilaizing it
######################################################################
api = Api(app,
          version='1.0.0',
          title='Product Demo REST API Service',
          description='This is a sample server Product server.',
          default='products',
          default_label='Products operations',
          # doc='/' # default also could use
          doc='/apidocs/'
          # prefix='/api'
         )

# Define the model so that the docs reflect what can be sent
product_model = api.model('Product', {'id': fields.Integer(required=True, description='The id of the product'),
                      'name': fields.String(required=True, description='The name of the product'),
                      'description': fields.String(required=True, description='Detailed information about the product'),
                      'category': fields.String(required=True, description='The category of the product'),
                      'price': fields.Integer(required=True, description='The price of the product'),
                      'condition': fields.String(required=True, description='The condition of the product'),
                      'inventory': fields.Integer(required=True, description='The inventory of the product'),
                      'review': fields.String(required=False, description='The review of the product'),
                      'rating': fields.Integer(required=True, description='The rating of the product'),
                      'hitCount': fields.Integer(required=True, description='The number of times product has been rated'),
                      'updatedDate': fields.String(required=False, description="Last updated date of product")
                     })

# query string arguments
product_arguments = reqparse.RequestParser()
product_arguments.add_argument('minimum', type=int, required=True)
product_arguments.add_argument('maximum', type=int, required=True)

product_arguments1 = reqparse.RequestParser()
# product_arguments1.add_argument('id', type=int, required=False)
product_arguments1.add_argument('name', type=str, required=False)
product_arguments1.add_argument('category', type=str, required = False)

product_arguments2 = reqparse.RequestParser()
product_arguments2.add_argument('id', type=int, required=True)
product_arguments2.add_argument('rating', type=int, required=True)

product_arguments3 = reqparse.RequestParser()
product_arguments3.add_argument('id', type=int, required=True)
product_arguments3.add_argument('rev', type=int, required=True)

ns = api.namespace("products", description="Products API")

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

@app.route('/healthcheck')
def healthcheck():
    """ Let them know our heart is still beating """
    return make_response(jsonify(status=200, message='Healthy'), status.HTTP_200_OK)


# @app.route('/products', methods=['GET'])
@api.route('/products', strict_slashes=False)
# @api.param('id', 'The Product identifier')
class ProductCollection(Resource):

    #########################
    # list all products
    #########################
    @api.doc('list_products')
    @api.expect(product_arguments1)
    @api.marshal_list_with(product_model)
    def get(self):
         """ Return all the products"""
         products = []
         # id = (product_arguments1.parse_args())['id']
         name = (product_arguments1.parse_args())['name']
         category = (product_arguments1.parse_args())['category']
         # name = request.args.get('name')
         app.logger.info(name)
         # category = request.args.get('category')
         # id = request.args.get("id")
         if name:
             products = Product.find_by_name(name)
         elif category:
             products = Product.find_by_category(category)
         # elif id:
         #     products = Product.find_by_id(id)
         else:
             products = Product.all()
         results = [product.serialize() for product in products]
         # return make_response(jsonify(results), status.HTTP_200_OK)
         return results,status.HTTP_200_OK

    #########################
    # create a product
    #########################
    @api.doc('create_products')
    @api.expect(product_model)
    @api.response(400,"Validation Error")
    @api.response(201,"Success")
    @api.marshal_with(product_model, code=201)
    def post(self):
        """
        Creates a Product
        This endpoint will create a Pet based the data in the body that is posted
        """
        check_content_type('application/json')
        product = Product(1,"","","",0,"",0,"",0)
        product.deserialize(api.payload)
        product.save()
        message = product.serialize()
        location_url = url_for('list_products_by_id', item_id=product.id, _external=True)
        # return make_response(jsonify(message), status.HTTP_201_CREATED,
        #                      {
        #                          'Location': location_url
        #                      })
        return product.serialize,status.HTTP_201_CREATED,{'Location':location_url }


@api.route('/products/<int:item_id>')
@api.param('item_id', 'The Product identifier')
class ProductResource(Resource):

    #########################
    # list products by ID
    #########################
    # @app.route('/products/<int:item_id>', methods=["GET"])
    @api.doc('list_products')
    @api.response(404, "Product Not Found")
    @api.marshal_with(product_model)
    def get(self,item_id):
        app.logger.info('Finding a Product with id [{}]'.format(item_id))
        product = Product.find_by_id(item_id)
        if product:
            message = product.serialize()
            return_code = status.HTTP_200_OK
        else:
            #message = {'error' : 'Product with id: %s was not found' % str(item_id)}
            api.abort(status.HTTP_404_NOT_FOUND,'Product with id: %s was not found' % str(item_id))
            # raise NotFound(message)
            ## return_code = status.HTTP_404_NOT_FOUND
        return message, return_code

    #########################
    # update product by ID
    #########################
    # @api.route("/products/<int:item_id>", )
    @api.doc('update_products')
    @api.expect(product_model)
    @api.response(404, "Product Not Found")
    @api.response(400, "Validation Error")
    @api.marshal_with(product_model)
    def put(self,item_id):
        app.logger.info("Fetching the product")
        check_content_type("application/json")
        product = Product.find_by_id(item_id)
        # app.logger.info(product.rating)
        # prevrating = product.rating
        if not product:
            api.abort(status.HTTP_404_NOT_FOUND,'Product with id: %s was not found' % str(item_id))
            # raise NotFound("Product with id {} not found".format(item_id))
        # app.logger.info(product.deserialize(request.get_json()))
        hitcount = product.updateCount
        product.deserialize(api.payload)
        product.id = item_id
        # app.logger.info(product.rating)
        product.rating = product.totalrating/(hitcount+1)
        product.update()
        # return make_response(jsonify(product.serialize()),status.HTTP_200_OK)
        return product.serialize(),status.HTTP_200_OK

    #########################
    # delete product by ID
    #########################
    @api.doc('delete_products')
    @api.response(204, "Product Deleted")
    def delete(self,item_id):
        app.logger.info("Deleting the product for the id provided")
        product = Product.find_by_id(item_id)
        # if not product:
        #     return make_response("Product does not exist", status.HTTP_204_NO_CONTENT)
        if product:
            product.delete()
        # return make_response(" ", status.HTTP_204_NO_CONTENT)
        return " ", status.HTTP_204_NO_CONTENT

@api.route('/products/latest')
# @api.param('id', 'The Product identifier')
class ProductSort(Resource):

    #########################
    # Sort products by date
    #########################
    @api.doc('sort_products')
    @api.marshal_list_with(product_model)
    def get():
        """List all the product by their updated date"""
        app.logger.info("List products by updated date")
        sorted_products = Product.sort_by_date()
        results = [ product.serialize() for product in sorted_products]
        # return make_response(jsonify(results), status.HTTP_200_OK)
        return results,status.HTTP_200_OK


# @app.route("/products/pricerange", methods=["GET"])

@api.route('/products/pricerange')
# @api.param('id', 'The Product identifier')
class ProductPrice(Resource):

    #########################
    # list products by price range
    #########################
    @api.doc('list_products_pricerange')
    @api.expect(product_arguments)
    @api.marshal_list_with(product_model)
    def get(self):
        app.logger.info("Fetching products by provided price range")
        # app.logger.info(request.args.get('minimum'))
        # minimum = request.args.get('minimum')
        # maximum = request.args.get('maximum')
        minimum = int((product_arguments.parse_args())['minimum'])
        maximum = int ((product_arguments.parse_args())['maximum'])
        tlist = list(Product.search_by_price(minimum,maximum))
        result = []
        for i in tlist:
            result.append(i.serialize())
        # app.logger.info(result)
        # return make_response(jsonify(result), status.HTTP_200_OK)
        return result, status.HTTP_200_OK



@api.route("/products/rating")
# @api.param('id1', 'The Product id ')
# @api.param('star1', 'The Product rating')
class ProductRating(Resource):

    #############################
    # update product rating by ID
    #############################
    @api.doc('update_product_rating')
    @api.expect(product_arguments2)
    @api.marshal_with(product_model)
    @api.response(404,"Product Not Found")
    def put(self):
        app.logger.info("Fetching the product")
        # item = request.args.get("id")
        # check_content_type("application/json")
        item = int((product_arguments2.parse_args())['id'])
        newrating = int ((product_arguments2.parse_args())['rating'])
        product = Product.find_by_id(item)
        # newrating = request.args.get('stars')
        # print(newrating)
        if not product:
            api.abort(status.HTTP_404_NOT_FOUND,'Product with id: %s was not found' % str(item_id))
            # raise NotFound("Product with id {} not found".format(item))
        # app.logger.info(product.deserialize(request.get_json()))
        # product.deserialize(request.get_json())
        # product.id = item_id
        # app.logger.info(product.rating)
        product.totalrating += int(newrating)
        # product.updateCount += 1
        product.rating = (int(product.totalrating)/(product.updateCount + 1))
        product.update()
        # return make_response(jsonify(product.serialize()),status.HTTP_200_OK)
        return product.serialize(),status.HTTP_200_OK


@api.route("/products/review")
# @api.param('id1', 'The Product id ')
# @api.param('star1', 'The Product rating')
class ProductReview(Resource):
    #############################
    # update product review by ID
    #############################
    # @app.route("/products/review", methods=["PUT"])
    @api.doc('update_product_rating')
    @api.expect(product_arguments3)
    @api.marshal_with(product_model)
    @api.response(404,"Product Not Found")
    def put(self, ):
        app.logger.info("Fetching the product")
        # item_id = request.args.get("id")
        item = int((product_arguments3.parse_args())['id'])
        check_content_type("application/json")
        product = Product.find_by_id(item_id)
        newreview =  str ((product_arguments2.parse_args())['rev'])
        print(newreview)
        if not product:
            api.abort(status.HTTP_404_NOT_FOUND,'Product with id: %s was not found' % str(item_id))
        if not product.review:
             product.review = str(newreview)
        else:
            product.review = str(product.review) + "|" + str(newreview)
        product.update()

        # return make_response(jsonify(product.serialize()),status.HTTP_200_OK)
        return product.serialize(),status.HTTP_200_OK


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
        print ('Setting up logging...')
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
