from flask import Flask
from flask_restplus import Api, Resource, fields, reqparse
# from app.model import Product

app = Flask(__name__)
api = Api(app, version='1.0', title='Sample API for NYU-DevOps-Products')

product_model = api.model('Product', {'id': fields.Integer(required=True, description='The id of the product'),
                              'name': fields.String(required=True, description='The name of the product'),
                              'description': fields.String(required=True, description='Detailed information about the product'),
                              'category': fields.String(required=True, description='The category of the product'),
                              'price': fields.Integer(required=True, description='The price of the product'),
                              'condition': fields.String(required=True, description='The condition of the product'),
                              'inventory': fields.Integer(required=True, description='The inventory of the product'),
                              'review': fields.String(required=False, description='The review of the product'),
                              'rating': fields.Integer(required=True, description='The rating of the product'),
                              'hitCount': fields.Integer(required=True, description='The number of times product has been rated')
                             })

products = []
product1 = {'id': 1, 'name': 'Desk', 'description': 'wooden study desk', 'category': 'Furniture', 'price': '50', 'condition': 'Boxed', 'inventory': '500', 'review': 'Great product', 'rating': '8','hitCount':'1'}
product2 = {'id': 2, 'name': 'Chair', 'description': 'mesh office chair', 'category': 'Furniture', 'price': '30', 'condition': 'Boxed', 'inventory': '1500', 'review': '', 'rating': '9','hitCount':'1'}
products.append(product1)
products.append(product2)
results = []

product_arguments = reqparse.RequestParser()
product_arguments.add_argument('minimum', type=int, required=True)
product_arguments.add_argument('maximum', type=int, required=True)

product_arguments1 = reqparse.RequestParser()
product_arguments1.add_argument('id', type=int, required=True)
product_arguments1.add_argument('stars', type=int, required=True, choices=[1,2,3,4,5,6,7,8,9,10])


@api.route('/products')
class ProductCollection(Resource):
    @api.marshal_with(product_model)
    def get(self):
        return products, 200

    @api.expect(product_model)
    def put(self):
        return api.payload, 200

    @api.expect(product_model)
    def post(self):
        new_product = api.payload
        products.append(new_product)
        return new_product, 201

    def delete(self):
	    return [], 204


@api.route('/products/<id>')
@api.doc(params={'id':'product id'})
class ProductCollection(Resource):
    def get(self, id):
        global results
        results2 = []
        for p in products:
            paramid = int(id)
            pid = int(p['id'])
            if(pid == paramid):
                print("Yayy")
                print((id))
                results2.append(p)
        return results2, 200


    # @api.route('/products', methods=['GET'])
    # @api.doc(params={'name':'product name', 'category':'product category'})
    # class ProductCollection(Resource):
    #     def get(self, name):
    #         return api.output(), 200
    #
    #
    # @api.route('/products', methods=['GET'])
    # @api.doc(params={'category':'product category'})
    # class ProductCollection(Resource):
    #     def get(self, category):
    #         return api.output(), 200
    #
    #
@api.route('/products/pricerange', methods=['GET'])
class ProductCollection(Resource):
    @api.expect(product_arguments, validate=True)
    def get(self):
        # print((product_arguments.parse_args())['minimum'])
        # print((product_arguments.parse_args())['maximum'])
        min = int((product_arguments.parse_args())['minimum'])
        max = int ((product_arguments.parse_args())['maximum'])
        global results
        results1=[]
        for p in products:
            print(min)
            price1 = int(p['price'])
            print(price1)
            print(max)
            if (price1 >= min):
                print ("yay1")
                if (price1 <= max):
                    results1.append(p)
                    print("Yayy")
                print(results1)
        return results1, 200
    #
    #

@api.route('/products/rating/<int:id1>/<int:star1>')
@api.param('id1', 'The Product id ')
@api.param('star1', 'The Product rating')
# @api.doc(params={'stars':'product rating'})
class ProductCollection(Resource):
    # @api.expect(product_arguments1, validate=True)
    def put(self, id1,star1):
        # print(product_arguments1)
        # p_id = int((product_arguments1.parse_args())['id'])
        product1 = []
        for p in products:
            pid = int(p['id'])
            print(pid)
            if (pid == id1):
                product1 = p
                break
        rating1 = int (product1['rating'])
        hit= int(product1['hitCount'])
        hit+=1
        product1['hitCount']=hit
        product1['rating']= int (rating1 + star1)/ int(product1['hitCount'])
        return product1,201

@api.route('/products/review/<int:id1>/<string:review1>')
@api.param('id1', 'The Product id ')
@api.param('review1', 'The Product review')
class ProductCollection(Resource):
    def put(self, id1,review1):
        product1 = []
        for p in products:
            pid = int(p['id'])
            if (pid == id1):
                product1 = p
                break
        reviews = str(product1['review'])
        product1['review'] = reviews + "|" + str (review1)
        return product1,201


#@api.route('/products/latest')
#@api.doc(params={'updateddate':'product update info'})
#class ProductCOllection(Resource):
#    def get(self):
#        sorted_products = Product.sort_by_date()
	#sorted_products = sorted(products, key='updateddate')
#	return sorted_products, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
