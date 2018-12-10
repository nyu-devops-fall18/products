#Copyright 2016, 2017 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Product API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
  codecov --token=$CODECOV_TOKEN
"""

import unittest
import os
import json
import logging
from flask_api import status    # HTTP Status Codes
from mock import MagicMock, patch
from app.model import Product, ValidationError, db
import app.service as service
import time

DATABASE_URI = os.getenv('DATABASE_URI', None)

######################################################################
#  T E S T   C A S E S
######################################################################
class TestProductServer(unittest.TestCase):
    """ Product Server Tests """

    @classmethod
    def setUpClass(cls):
        """ Run once before all tests """
        service.app.debug = False
        service.initialize_logging(logging.INFO)
        # Set up the test database
        if DATABASE_URI:
            service.app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
        service.init_db()

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        """ Runs before each test """
        # service.init_db()
        db.drop_all()    # clean up the last tests
        db.create_all()  # create new tables
        Product(pid=1,pname="Athens Table", pdesc='Stupid Table', pcat="Table", pprice=20, pcond="Boxed",pinv=2, prev="", prat=5).save()
        Product(pid=2,pname="Rome Chair", pdesc='Stupid Chair', pcat="Chair", pprice=40, pcond="Boxed", pinv=2, prev="",prat=8).save()
        self.app = service.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_index(self):
        """ Test the Home Page """
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # data = json.loads(resp.data)
        # self.assertEqual(data['name'], 'Product Demo REST API Service')

    def test_healthcheck(self):
        """ Test the Health Check page """
        resp = self.app.get('/healthcheck')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_product_list(self):
        """ Get a list of Products """
        resp = self.app.get('/products')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(len(data), 2)

    def test_get_product_list_by_date(self):
        """ Get a list of Products by date order"""
        products = Product.sort_by_date()
        results = [ product.serialize() for product in products]
        resp = self.app.get('/products/latest')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        # print(data)
        # print(products)
        # print(results)
        self.assertEqual(data, results)


    def test_get_product(self):
        """ Get a single Product """
        # get the id of a product
        product = Product.find_by_name('Athens Table')[0]
        resp = self.app.get('/products/{}'.format(product.id),
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(data['name'], product.name)

    def test_get_product_not_found(self):
        """ Get a Product thats not found """
        resp = self.app.get('/products/0')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_product_not_found_delete(self):
        """ Get a Product thats not found in Delete Request """
        resp = self.app.delete('/products/0')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_product(self):
        """ Create a new Product """
        # save the current number of products for later comparison
        product_count = self.get_product_count()
        # add a new product
        new_product = dict(id=3, name='Greek Table', description='Its a Table', category="Table", price=12, condition="Boxed", inventory=2, review="Amazing", rating=2)
        data = json.dumps(new_product)
        resp = self.app.post('/products',
                             data=data,
                             content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get('Location', None)
        self.assertTrue(location != None)
        # Check the data is correct
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['name'], 'Greek Table')
        # check that count has gone up and includes sammy
        resp = self.app.get('/products')
        # print 'resp_data(2): ' + resp.data
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), product_count + 1)
        self.assertIn(new_json, data)

    def test_create_product_bad_request(self):
        """ Create a new Product with a bad data"""
        # save the current number of products for later comparison
        product_count = self.get_product_count()
        # add a new product
        new_product = dict(id=3, name='Greek Table', category="Table", price=12, condition="Boxed", inventory=2, review="Amazing", rating=2)
        data = json.dumps(new_product)
        resp = self.app.post('/products',
                             data=data,
                             content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        # Make sure location header is set
        location = resp.headers.get('Location', None)
        self.assertTrue(location is None)

    def test_update_product(self):
        """ Update an existing Product """
        product = Product.find_by_name('Athens Table')[0]
        new_product = dict(id=1,name='Athens Table', description='Stupid Table', category="Fancy Table",price=20, condition="Boxed", inventory=2, review="So so", rating=8)
        data = json.dumps(new_product)
        resp = self.app.put('/products/{}'.format(product.id),
                            data=data,
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['category'], 'Fancy Table')

    def test_update_product_bad_request(self):
        """ Update an existing Product with bad data"""
        product = Product.find_by_name('Athens Table')[0]
        new_product = dict(id=1,name='Athens Table', category="Fancy Table", price=20, condition="Boxed", inventory=2,
                           review="So so", rating=8)
        data = json.dumps(new_product)
        resp = self.app.put('/products/{}'.format(product.id),
                            data=data,
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_product_rating(self):
        """ Update an existing Product Rating """
        product = Product.find_by_name('Athens Table')[0]
        # new_product = dict(id=1,name='Athens Table', description='Stupid Table', category="Fancy Table",price=20, condition="Boxed", inventory=2, review="", rating=8)
        # data = json.dumps(new_product)
        resp = self.app.put('/products/rating',
                            query_string='id=1&stars=9',
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['rating'], 7)

    def test_update_product_rating_invalid_id(self):
        """ Update an existing Product Rating with invalid ID"""
        resp = self.app.put('/products/rating',
                            query_string='id=0&stars=1',
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_product_rating_missing_param(self):
        """ Update an existing Product Rating with missing parameter"""
        resp = self.app.put('/products/rating',
                            query_string='id=1',
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_product_rating_invalid_rating(self):
        """ Update an existing Product Rating with invalid rating"""
        resp = self.app.put('/products/rating',
                            query_string='id=1&stars=21',
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_product_rating_invalid_rating_type(self):
        """ Update an existing Product Rating with invalid rating type"""
        resp = self.app.put('/products/rating',
                            query_string='id=1&stars=sdaf',
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_product_review(self):
        """ Update an existing Product Review """
        product = Product.find_by_name('Athens Table')[0]
        resp = self.app.put('/products/review',
                            query_string='id=1&newrev=Average',
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['review'], 'Average')
        product = Product.find_by_name('Athens Table')[0]
        resp = self.app.put('/products/review',
                            query_string='id=1&newrev=Awesome',
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['review'], 'Average|Awesome')

    def test_update_product_review_invalid_id(self):
        """ Update an existing Product Review with invalid ID"""
        resp = self.app.put('/products/review',
                            query_string='id=0&newrev=Average',
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_product_review_missing_param(self):
        """ Update an existing Product Review with missing param"""
        resp = self.app.put('/products/review',
                            query_string='id=1',
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_product(self):
        """ Delete a Product """
        product = Product.find_by_name('Athens Table')[0]
        # save the current number of products for later comparison
        product_count = self.get_product_count()
        resp = self.app.delete('/products/{}'.format(product.id),
                               content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        new_count = self.get_product_count()
        self.assertEqual(new_count, product_count - 1)

    def test_delete_all_products(self):
        """ Delete all Products """
        # save the current number of products for later comparison
        # product_count = self.get_product_count()
        resp = self.app.delete('/products',
                               content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        # new_count = self.get_product_count()
        # self.assertEqual(new_count, 0)

    def test_query_product_list_by_name(self):
        """ Query Products by Name """
        resp = self.app.get('/products',
                            query_string='name=Rome Chair')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreater(len(resp.data), 0)
        self.assertIn("Chair", resp.data)
        self.assertNotIn('Table', resp.data)
        data = json.loads(resp.data)
        query_item = data[0]
        self.assertEqual(query_item['name'], 'Rome Chair')


    def test_query_product_list_by_category(self):
        """ Query Products by Category """
        resp = self.app.get('/products',
                            query_string='category=Chair')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreater(len(resp.data), 0)
        self.assertIn("Rome Chair", resp.data)
        self.assertNotIn('Table', resp.data)
        data = json.loads(resp.data)
        query_item = data[0]
        self.assertEqual(query_item['category'], 'Chair')

    def test_query_product_list_by_pricerange(self):
        """ Query Products by PriceRange """
        resp = self.app.get('/products/pricerange',
                            query_string='minimum=30&maximum=50')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreater(len(resp.data), 0)
        self.assertIn("Rome Chair", resp.data)
        self.assertNotIn('Table', resp.data)
        data = json.loads(resp.data)
        query_item = data[0]
        self.assertEqual(query_item['category'], 'Chair')

    def test_method_not_allowed(self):
        resp = self.app.put('/products')
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # @patch('app.service.Product.find_by_name')
    # def test_bad_request(self, bad_request_mock):
    #     """ Test a Bad Request error from Find By Name """
    #     bad_request_mock.side_effect = ValidationError()
    #     resp = self.app.get('/products', query_string='name=Rome Chair')
    #     self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('app.service.Product.update')
    def test_bad_request_header(self, invalid_header_mock):
        """ Test a Bad Request error from Update"""
        resp = self.app.put('/products/1', headers={'Content-Type': 'xml'})
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    @patch('app.service.Product.update')
    def test_bad_request_product_404(self, bad_request_mock):
        """ Test a Bad Request error from Update due to invalid product"""
        resp = self.app.put('/products/0', headers={'Content-Type': 'application/json'})
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    @patch('app.service.Product.find_by_name')
    def test_mock_search_data(self, product_find_mock):
        """ Test showing how to mock data """
        product_find_mock.return_value = [MagicMock(serialize=lambda: {'name': 'Rome Chair'})]
        resp = self.app.get('/products', query_string='name=Rome Chair')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @patch('app.service.Product.find_by_name')
    def test_search_bad_data(self, product_find_mock):
        """ Test a bad search that returns bad data """
        product_find_mock.return_value = None
        resp = self.app.get('/products', query_string='name=Rome Chair')
        self.assertEqual(resp.status_code,status.HTTP_500_INTERNAL_SERVER_ERROR)

######################################################################
# Utility functions
######################################################################

    def get_product_count(self):
        """ save the current number of products """
        resp = self.app.get('/products')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        return len(data)


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
