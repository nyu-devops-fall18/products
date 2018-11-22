
from flask import Flask
from flask_restplus import Api, Resource, fields, reqparse
#from app.model import Product

app = Flask(__name__)
api = Api(app, version='1.0', title='Sample API for NYU-DevOps-Products')

product_model = api.model('Product', {'id': fields.String(required=True, description='The id of the product'),
                              'name': fields.String(required=True, description='The name of the product'),
                              'description': fields.String(required=True, description='Detailed information about the product'),
                              'category': fields.String(required=True, description='The category of the product'),
                              'price': fields.String(required=True, description='The price of the product'),
                              'condition': fields.String(required=True, description='The condition of the product'),
                              'inventory': fields.String(required=True, description='The inventory of the product'),
                              'review': fields.String(required=False, description='The review of the product'),
                              'stars': fields.String(required=True, description='The rating of the product'),
                              'updateddate': fields.String(required=False),
                              'updateCount': fields.String(required=False, description='The most recent count of the product'),
                              'totalrating': fields.String(required=False, description='The total rating of the product')
                             })

products = [{'id': 1, 'name': 'Desk', 'description': 'wooden study desk', 'category': 'Furniture', 'price': '50', 'condition': 'Boxed', 'inventory': '500', 'review': 'Great product', 'stars': '8'}]
product = {'id': 2, 'name': 'Chair', 'description': 'mesh office chair', 'category': 'Furniture', 'price': '30', 'condition': 'Boxed', 'inventory': '1500', 'review': '', 'stars': '9'}
products.append(product)

product_arguments = reqparse.RequestParser()
product_arguments.add_argument('minimum', type=int, required=True)
product_arguments.add_argument('maximum', type=int, required=True)

product_arguments1 = reqparse.RequestParser()
product_arguments.add_argument('id', type=int, required=True)
product_arguments.add_argument('rating', type=int, required=True, choices=[1,2,3,4,5,6,7,8,9,10])


@api.route('/products')
class ProductCollection(Resource):
    @api.marshal_with(product_model)
    def get(self):
        return products, 200

    @api.expect(product_model)

    def put(self):
        return products, 202

    def post(self):
        new_product = api.payload
        products.append(new_product)
        return new_product, 201

    def delete(self):
	return products, 204


@api.route('/products?id=id')
@api.doc(params={'id':'product id'})
class ProductCOllection(Resource):
    def get(self, id):
	return products, 200

    def put(self, id):
	return products, 202

    def delete(self, id):
	return products, 204


@api.route('/products?name=name')
@api.doc(params={'name':'product name'})
class ProductCOllection(Resource):
    def get(self, name):
	return products, 200


@api.route('/products?category=category')
@api.doc(params={'category':'product category'})
class ProductCOllection(Resource):
    def get(self, category):
	return products, 200


@api.route('/products/pricerange')
class ProductCOllection(Resource):
    @api.expect(product_arguments, validate=True)
    def get(self):
	return products, 200


#@api.route('/products/rating/1', methods=['PUT'])
#@api.doc(params={'stars':'product rating'})
#class ProductCOllection(Resource):
    #@api.expect(product_arguments1, validate=True)
#    def put(self):
#	return products, 202


#@api.route('/products/latest')
#@api.doc(params={'updateddate':'product update info'})
#class ProductCOllection(Resource):
#    def get(self):
#        sorted_products = Product.sort_by_date()
	#sorted_products = sorted(products, key='updateddate')
#	return sorted_products, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
