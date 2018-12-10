# Products
[![Build Status](https://travis-ci.org/nyu-devops-fall18/products.svg?branch=master)](https://travis-ci.org/nyu-devops-fall18/products)
[![codecov](https://codecov.io/gh/nyu-devops-fall18/products/branch/master/graph/badge.svg)](https://codecov.io/gh/nyu-devops-fall18/products)

# Service Descriptions and Endpoints 
The products resource represents the store items that the customer can perform the following operations:
* List All products: the mainpage /products
* List products by ID: /products?id=<int:id>
* List products by date: list up all the products in a descending order
* List products by category: /products?category=<str:category>
* List products by name: /products?name=<str:name>
* List products by price range: /products/pricerange?minimum=<int:minimum>&?maximum=<int:maximum>
* Give product a rating: /products/rating/<int:id>/<int:star>
* Give product a review: products/review/<int:id>/<str:review>'

On the other hand, developers can:
* Create a new product
* Update a product
* Delete a product

# How to run the service on your local PC
Step1. Preparations
To run our services on your local PC, you need to download Gitbash, Vagrant and Virtualbox. The download links are:
- Gitbash: https://git-scm.com/download
- Vagrant: https://www.vagrantup.com/
- Virtualbox: https://www.virtualbox.org/
Please check out if your PC is 32-bit or 64-bit to make sure your download the correct install file.

Step2. Run the Services
Please open Gitbash and run the following commands:
```shell

git clone https://github.com/nyu-devops-fall18/products.git  
- Downloads all the codes of our services from Github

cd products     
- Go to folder that contains the Vagrantfile

vagrant up
- To create the evironment needed for our services

vagrant ssh
- Connect to the virutalbox of our service using secure channel

cd /vagrant
- Go inside the virtual box 

honcho start
- Start the services. TO check it out, go to the browser and input the address: http://localhost:5000.
Try the following urls:
e.g.1 to list all the products, please try link: http://localhost:5000/products <br>
e.g.2 to sort all the products by date, please try link: http://localhost:5000/products/latest <br>
e.g.3 to search a product by name, please try link: http://localhost:5000/products?name=desk <br>
e.g.4 to search a product by category, please try link: http://localhost:5000/products?category=clothing <br>

```

# Running TDD Unit Tests
Perform the same steps as above, till cd /vagrant and then run the following command:
```shell
nosetests
```

# Running BDD Integration Tests
Perform the same steps as above, till cd /vagrant and then run the following:
```shell
honcho start &
behave
```
To stop the app, do the following:
```shell
fg


<ctrl + c>

```

# Services Running on Cloud
You can also directly visit our services on cloud.
https://nyu-product-service-f18-prod.mybluemix.net/
