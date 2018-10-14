# Copyright 2016, 2017 John J. Rofrano. All Rights Reserved.
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

from app.productmodel import Product, ValidationError, db
import app.productservice as service

DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///../db/test.db')

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
        service.app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        """ Runs before each test """
        service.init_db()
        db.drop_all()    # clean up the last tests
        db.create_all()  # create new tables
        Product(pid=1,pname='Athens Table', pdesc='Stupid Table', pcat="Table", pcond="Boxed", pprice=20, prat=5, prev="",pinv=2).save()
        Product(pid=2,pname='Rome Chair', pdesc='Stupid Chair', pcat="Chair", pcond="Boxed", pprice=40, prat=8, prev="",pinv=2).save()
        self.app = service.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_index(self):
        """ Test the Home Page """
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(data['name'], 'Product Demo REST API Service')

    def test_get_product_list(self):
        """ Get a list of Products """
        resp = self.app.get('/products')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(len(data), 2)

    def test_get_product(self):
        """ Get a single Product """
        # get the id of a pet
        pet = Product.find_by_name('Athens Table')[0]
        resp = self.app.get('/products/{}'.format(Product.id),
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(data['name'], Product.name)

    def test_get_product_not_found(self):
        """ Get a Product thats not found """
        resp = self.app.get('/products/0')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_product(self):
        """ Create a new Product """
        # save the current number of pets for later comparison
        product_count = self.get_product_count()
        # add a new pet
        new_product = dict(pid=3, pname='Greek Table', pdesc='Its a Table', pcat="Table", pcond="Boxed", pprice=12, prat=5, prev="",pinv=2)
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
        self.assertEqual(new_json['pname'], 'Greek Table')
        # check that count has gone up and includes sammy
        resp = self.app.get('/products')
        # print 'resp_data(2): ' + resp.data
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), product_count + 1)
        self.assertIn(new_json, data)

    def test_update_product(self):
        """ Update an existing Product """
        product = Product.find_by_name('Greek Table')[0]
        new_product = dict(pid=3,pname='Greek Table', pdesc='Its a Table', pcat=" Fancy Table", pcond="Boxed", pprice=12, prat=5, prev="", pinv=2)
        data = json.dumps(new_product)
        resp = self.app.put('/pets/{}'.format(product.id),
                            data=data,
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['category'], 'Fancy Table')

    def test_delete_product(self):
        """ Delete a Product """
        product = Product.find_by_name('Greek Table')[0]
        # save the current number of products for later comparrison
        product_count = self.get_product_count()
        resp = self.app.delete('/products/{}'.format(product.id),
                               content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        new_count = self.get_product_count()
        self.assertEqual(new_count, product_count - 1)

    def test_query_pet_list_by_category(self):
        """ Query Products by Category """
        resp = self.app.get('/products',
                            query_string='category=Fancy Table')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreater(len(resp.data), 0)
        self.assertIn('Greek Table', resp.data)
        self.assertNotIn('Fancy Table', resp.data)
        data = json.loads(resp.data)
        query_item = data[0]
        self.assertEqual(query_item['category'], 'Fancy Table')

    # @patch('service.Pet.find_by_name')
    # def test_bad_request(self, bad_request_mock):
    #     """ Test a Bad Request error from Find By Name """
    #     bad_request_mock.side_effect = DataValidationError()
    #     resp = self.app.get('/pets', query_string='name=fido')
    #     self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
    #
    # @patch('service.Pet.find_by_name')
    # def test_mock_search_data(self, pet_find_mock):
    #     """ Test showing how to mock data """
    #     pet_find_mock.return_value = [MagicMock(serialize=lambda: {'name': 'fido'})]
    #     resp = self.app.get('/pets', query_string='name=fido')
    #     self.assertEqual(resp.status_code, status.HTTP_200_OK)


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
