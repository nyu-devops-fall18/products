# from flask import Flask
# from flask_restplus import Api, Resource, fields, reqparse, abort
# from datetime import datetime
# import json
#
# app = Flask(__name__)
# api = Api(app, version='1.0', title='Sample API for NYU-DevOps-Products')
#
# product_model = api.model('Product', {'id': fields.Integer(required=True, description='The id of the product'),
#                               'name': fields.String(required=True, description='The name of the product'),
#                               'description': fields.String(required=True, description='Detailed information about the product'),
#                               'category': fields.String(required=True, description='The category of the product'),
#                               'price': fields.Integer(required=True, description='The price of the product'),
#                               'condition': fields.String(required=True, description='The condition of the product'),
#                               'inventory': fields.Integer(required=True, description='The inventory of the product'),
#                               'review': fields.String(required=False, description='The review of the product'),
#                               'rating': fields.Integer(required=True, description='The rating of the product'),
#                               'hitCount': fields.Integer(required=True, description='The number of times product has been rated'),
#                               'updatedDate': fields.String(required=False, description="Last updated date of product")
#                              })
#
# products = []
# product1 = {'id': 1, 'name': 'Desk', 'description': 'wooden study desk', 'category': 'Furniture', 'price': '50', 'condition': 'Boxed', 'inventory': '500', 'review': 'Great product', 'rating': '8','hitCount':'1', 'updatedDate': str(datetime.now())}
# product2 = {'id': 2, 'name': 'Chair', 'description': 'mesh office chair', 'category': 'Office', 'price': '30', 'condition': 'Boxed', 'inventory': '1500', 'review': '', 'rating': '9','hitCount':'1', 'updatedDate': str(datetime.now())}
# products.append(product1)
# products.append(product2)
# results = []
#
# product_arguments = reqparse.RequestParser()
# product_arguments.add_argument('minimum', type=int, required=True)
# product_arguments.add_argument('maximum', type=int, required=True)
#
# product_arguments1 = reqparse.RequestParser()
# product_arguments1.add_argument('id', type=int, required=False)
# product_arguments1.add_argument('name', type=str, required=False)
# product_arguments1.add_argument('category', type=str, required = False)
#
# ns = api.namespace("products", description="Products API")
#
#
# @ns.route('')
# class ProductCollection(Resource):
#     # @api.marshal_with(product_model)
#     @api.expect(product_arguments1)
#     def get(self):
#         try:
#             # print("1")
#             id = (product_arguments1.parse_args())['id']
#             name = (product_arguments1.parse_args())['name']
#             cat = (product_arguments1.parse_args())['category']
#             print("1")
#             print(id)
#             print(name)
#             print(cat)
#             resultsprod = []
#             if(id):
#                 print("2")
#                 for p in products:
#                     paramid = int(id)
#                     pid = int(p['id'])
#                     if (pid == paramid):
#                         print("OK")
#                         print((id))
#                         resultsprod.append(p)
#                         break
#             elif (name):
#                 print("3")
#                 for p in products:
#                     paramname = str(name)
#                     pname = str(p['name'])
#                     if (pname == paramname):
#                         print("OK")
#                         print((name))
#                         resultsprod.append(p)
#                         break
#             elif (cat):
#                 print("4")
#                 for p in products:
#                     paramcat = str(cat)
#                     pcat = str(p['category'])
#                     if (pcat == paramcat):
#                         print("OK")
#                         print((cat))
#                         resultsprod.append(p)
#                         break
#             else:
#                 print("5")
#                 return products, 200
#
#             return resultsprod, 200
#         except Exception as e:
#             # return products, 200
#             print(e)
#
#     @api.expect(product_model)
#     def put(self):
#         return api.payload, 200
#
#
#     @api.expect(product_model)
#     def post(self):
#         new_product = api.payload
#         products.append(new_product)
#         return new_product, 201
#
#     def delete(self):
# 	    return [], 204
#
#
# @ns.route('/pricerange', methods=['GET'])
# class ProductCollection(Resource):
#     @api.expect(product_arguments, validate=True)
#     def get(self):
#         # print((product_arguments.parse_args())['minimum'])
#         # print((product_arguments.parse_args())['maximum'])
#         min = int((product_arguments.parse_args())['minimum'])
#         max = int ((product_arguments.parse_args())['maximum'])
#         global results
#         results1=[]
#         for p in products:
#             print(min)
#             price1 = int(p['price'])
#             print(price1)
#             print(max)
#             if (price1 >= min):
#                 print ("OK")
#                 if (price1 <= max):
#                     results1.append(p)
#                     print("OK as well")
#                 print(results1)
#         return results1, 200
#
#
# @ns.route('/rating/<int:id1>/<int:star1>')
# @api.param('id1', 'The Product id ')
# @api.param('star1', 'The Product rating')
# # @api.doc(params={'stars':'product rating'})
# class ProductCollection(Resource):
#     # @api.expect(product_arguments1, validate=True)
#     def put(self, id1,star1):
#         # print(product_arguments1)
#         # p_id = int((product_arguments1.parse_args())['id'])
#         product1 = []
#         for p in products:
#             pid = int(p['id'])
#             print(pid)
#             if (pid == id1):
#                 product1 = p
#                 break
#         rating1 = int (product1['rating'])
#         hit= int(product1['hitCount'])
#         hit+=1
#         product1['hitCount']=hit
#         product1['rating']= int (rating1 + star1)/ int(product1['hitCount'])
#         product1['updatedDate'] = str(datetime.now())
#         return product1,201
#
# @ns.route('/review/<int:id1>/<string:review1>')
# @api.param('id1', 'The Product id ')
# @api.param('review1', 'The Product review')
# class ProductCollection(Resource):
#     def put(self, id1,review1):
#         product1 = []
#         for p in products:
#             pid = int(p['id'])
#             if (pid == id1):
#                 product1 = p
#                 break
#         reviews = str(product1['review'])
#         product1['review'] = reviews + "|" + str (review1)
#         product1['updatedDate'] = str(datetime.now())
#         return product1,201
#
#
# @ns.route('/latest')
# class ProductCollection(Resource):
#    def get(self):
#        data = {}
#        i = 0
#        for p in products:
#            data[p['id']] = p
#        return list(sorted(data.values(), key=lambda item: item['updatedDate'], reverse=True)), 200
#
#
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
