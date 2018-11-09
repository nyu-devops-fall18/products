# Products
[![Build Status](https://travis-ci.org/nyu-devops-fall18/products.svg?branch=master)](https://travis-ci.org/nyu-devops-fall18/products)
[![codecov](https://codecov.io/gh/nyu-devops-fall18/products/branch/master/graph/badge.svg)](https://codecov.io/gh/nyu-devops-fall18/products)

# Service Description
The products resource represents the store items that the customer can perform the following operations: 
* List All products
* List products by ID
* List products by date (i.e. sort by date)
* List products by category
* List products by name
* List products by price range
* Give product a rating
* Give product a review

On the other hand, developers can:
* Create a new product
* Update a product
* Delete a product

# How to run the service
Please run the following commands:
```
git clone https://github.com/nyu-devops-fall18/products.git  
cd products     
vagrant up
vagrant ssh
cd /vagrant
python run.py   
```
e.g.1 to list all the products, please try link: http://localhost:5000/products <br>
e.g.2 to sort all the products by date, please try link: http://localhost:5000/products/latest <br>
e.g.3 to search a product by name, please try link: http://localhost:5000/products?name=desk <br>
e.g.4 to search a product by category, please try link: http://localhost:5000/products?category=clothing <br>

# Run Unit Tests
Perform the same steps as above, till cd /vagrant and then run the following command:
```
nosetests
```
