# PRODUCTS
[![Build Status](https://travis-ci.org/nyu-devops-fall18/products.svg?branch=master)](https://travis-ci.org/nyu-devops-fall18/products)
[![codecov](https://codecov.io/gh/nyu-devops-fall18/products/branch/master/graph/badge.svg)](https://codecov.io/gh/nyu-devops-fall18/products)

#SERVICE DESCRIPTION -- SERVICE

The products resource represents the store items that the customer can perform the following operations: 
(1) List All products
(2) List products by ID
(3) List products by date (i.e. sort by date)
(4) List products by category
(5) List products by name
(6) List products by price range
(7) Give product a rating
(8) Give product a review comment

On the other hand, developers can:
(1) Create a new product
(2) Update a product
(3) Delete a product
Each product should have a unique id (perhaps a SKU - Stock Keeping Unit), a name, description, price and others attributes like perhaps an image, ratings and reviews.


#HOW TO RUN THE SERVICE
Please run the following commands:
git clone https://github.com/nyu-devops-fall18/products.git  #Download git repo
cd /product     #Make sure Vagrantfile is in the folder
vagrant up
vagrant ssh
cd /vagrant
python run.py   #Flask will run on your localhost

e.g.1 to list up all the product, please try link: http://localhost:5000/products
e.g.2 to sort all the products by date, please try link: http://localhost:5000/products/latest
e.g.3 to search a product by name, please try link: http://localhost:5000/products?name=desk
e.g.4 to search a product by category, please try link: http://localhost:5000/products?category=clothing 

#RUN UNIT TEST
Please run command:
nosetests

