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
Test cases for Product Model

Test cases can be run with:
  nosetests
  coverage report -m
"""

import unittest
import os
from app.productmodel import Product, ValidationError, db
from app import app

DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///../db/test.db')

######################################################################
#  T E S T   C A S E S
######################################################################
class TestProducts(unittest.TestCase):
    """ Test Cases for Products """

    @classmethod
    def setUpClass(cls):
        """ These run once per Test suite """
        app.debug = False
        # Set up the test database
        app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        Product.init_db(app)
        db.drop_all()    # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_a_product(self):
        """ Create a product and assert that it exists """
        product = Product(1, "Couch", "White couch", "Furniture", 200, "Boxed", 50, " ", 8)
        self.assertTrue(product != None)
        self.assertEqual(product.id, 1)
        self.assertEqual(product.name, "Couch")
        self.assertEqual(product.category, "Furniture")
        self.assertEqual(product.description, "White couch")
        self.assertEqual(product.price, 200)
        self.assertEqual(product.condition, "Boxed")
        self.assertEqual(product.inventory, 50)
        self.assertEqual(product.rating, 8)

    def test_add_a_product(self):
        """ Create a product and add it to the database """
        products = Product.all()
        self.assertEqual(products, [])
        product = Product(1, "Couch", "White couch", "Furniture", 200, "Boxed", 50, " ", 8)
        self.assertTrue(product != None)
        self.assertEqual(product.id, 1)
        product.save()
        # Assert that it was assigned an id and shows up in the database
        self.assertEqual(product.id, 1)
        products = Product.all()
        self.assertEqual(len(products), 1)

    def test_update_a_product(self):
        """ Update a Product """
        product = Product(1, "Couch", "White couch", "Furniture", 200, "Boxed", 50, " ", 8)
        product.save()
        self.assertEqual(product.id, 1)
        # Change it and save it
        product.category = "Home"
        product.update()
        self.assertEqual(product.id, 1)
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        products = Product.all()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].category, "Home")

    def test_delete_a_product(self):
        """ Delete a Product """
        product = Product(1, "Couch", "White couch", "Furniture", 200, "Boxed", 50, " ", 8)
        product.save()
        self.assertEqual(len(Product.all()), 1)
        # delete the product and make sure it isn't in the database
        product.delete()
        self.assertEqual(len(Product.all()), 0)

    def test_serialize_a_product(self):
        """ Test serialization of a Product """
        product = Product(1, "Couch", "White couch", "Furniture", 200, "Boxed", 50, " ", 8)
        data = product.serialize()
        self.assertNotEqual(data, None)
        self.assertIn('id', data)
        self.assertEqual(data['id'], 1)
        self.assertIn('name', data)
        self.assertEqual(data['name'], "Couch")
        self.assertIn('category', data)
        self.assertEqual(data['category'], "Furniture")
        self.assertIn('description', data)
        self.assertEqual(data['description'], "White couch")
        self.assertIn('price', data)
        self.assertEqual(data['price'], 200)
        self.assertIn('condition', data)
        self.assertEqual(data['condition'], "Boxed")
        self.assertIn('inventory', data)
        self.assertEqual(data['inventory'], 50)
        self.assertIn('rating', data)
        self.assertEqual(data['rating'], 8)

    def test_deserialize_a_product(self):
        """ Test deserialization of a Product """
        data = {"id": 1, "name": "Couch", "description": "White couch", "category": "Furniture", "price": 200, "condition": "Boxed", "inventory": 50, "rating": 8, "review": " "}
        product = Product(1,"","","",0,"",0,"",0)
        product.deserialize(data)
        self.assertIsNot(product, None)
        self.assertEqual(product.id, 1)
        self.assertEqual(product.name, "Couch")
        self.assertEqual(product.category, "Furniture")
        self.assertEqual(product.description, "White couch")
        self.assertEqual(product.price, 200)
        self.assertEqual(product.condition, "Boxed")
        self.assertEqual(product.inventory, 50)
        self.assertEqual(product.rating, 8)

    def test_deserialize_bad_data(self):
        """ Test deserialization of bad data """
        data = "this is not a dictionary"
        product = Product(1,"","","",0,"",0,"",0)
        self.assertRaises(ValidationError, product.deserialize, data)

    def test_deserialize_bad_data_missing_arg(self):
        """ Test deserialization of missing arg """
        data = {"id": 1, "name": "Couch", "category": "Furniture", "price": 200, "condition": "Boxed", "inventory": 50, "rating": 8, "review": " "}
        product = Product(1,"","","",0,"",0,"",0)
        self.assertRaises(ValidationError, product.deserialize, data)

    def test_find_by_id(self):
        """ Find a Product by ID """
        Product(1, "Couch", "White couch", "Furniture", 200, "Boxed", 50, " ", 8).save()
        table = Product(2, "Table", "Oak table", "Home", 150, "Boxed", 100, " ", 7)
        table.save()
        product = Product.find_by_id(table.id)
        self.assertIsNot(product, None)
        self.assertEqual(product.id, table.id)
        self.assertEqual(product.name, "Table")
        self.assertEqual(product.category, "Home")
        self.assertEqual(product.description, "Oak table")
        self.assertEqual(product.price, 150)
        self.assertEqual(product.condition, "Boxed")
        self.assertEqual(product.inventory, 100)
        self.assertEqual(product.rating, 7)

    def test_find_by_category(self):
        """ Find Products by Category """
        Product(1, "Couch", "White couch", "Furniture", 200, "Boxed", 50, " ", 8).save()
        Product(2, "Table", "Oak table", "Home", 150, "Boxed", 100, " ", 7).save()
        products = Product.find_by_category("Furniture")
        self.assertEqual(products[0].id, 1)
        self.assertEqual(products[0].category, "Furniture")
        self.assertEqual(products[0].name, "Couch")
        self.assertEqual(products[0].description, "White couch")
        self.assertEqual(products[0].price, 200)
        self.assertEqual(products[0].condition, "Boxed")
        self.assertEqual(products[0].inventory, 50)
        self.assertEqual(products[0].rating, 8)

    def test_find_by_name(self):
        """ Find a Product by Name """
        Product(1, "Couch", "White couch", "Furniture", 200, "Boxed", 50, " ", 8).save()
        Product(2, "Table", "Oak table", "Furniture", 150, "Boxed", 100, " ", 7).save()
        products = Product.find_by_name("Couch")
        self.assertEqual(products[0].id, 1)
        self.assertEqual(products[0].category, "Furniture")
        self.assertEqual(products[0].name, "Couch")
        self.assertEqual(products[0].description, "White couch")
        self.assertEqual(products[0].price, 200)
        self.assertEqual(products[0].condition, "Boxed")
        self.assertEqual(products[0].inventory, 50)
        self.assertEqual(products[0].rating, 8)


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
