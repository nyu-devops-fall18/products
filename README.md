# Products
[![Build Status](https://travis-ci.org/nyu-devops-fall18/products.svg?branch=master)](https://travis-ci.org/nyu-devops-fall18/products)
[![codecov](https://codecov.io/gh/nyu-devops-fall18/products/branch/master/graph/badge.svg)](https://codecov.io/gh/nyu-devops-fall18/products)

# Service Descriptions and Endpoints 
The following operations can be performed on the products service:
* Create a new product: [POST] /products
* Update a product: [PUT] /products/<int:id>
* Delete a product: [DELETE] /products/<int:id>
* Delete all products: [DELETE] /products
* List all products: [GET] /products
* List products by ID: [GET] /products/<int:id>
* List products by category: [GET] /products?category=<str:category>
* List products by name: [GET] /products?name=<str:name>
* List products by price range: [GET] /products/pricerange?minimum=<int:minimum>&?maximum=<int:maximum>
* List all products in descending order of date: [GET] /products/latest
* Give product a rating: [PUT] /products/rating?id=<int:id>&stars=<int:stars>
* Give product a review: [PUT] /products/review?<int:id>&newrev<str:review>

# How to run the service on your local PC
Step1. Prerequisites
To run our services on your local PC, you need to download Gitbash, Vagrant and Virtualbox. The download links are:
- Gitbash: https://git-scm.com/download
- Vagrant: https://www.vagrantup.com/
- Virtualbox: https://www.virtualbox.org/
Please check out if your PC is 32-bit or 64-bit to make sure your download the correct install file.

Step2. Run the Services
Please open Gitbash (for Windows) or terminal (others) and run the following commands:
```shell
# Downloads all the codes of our services from Github
git clone https://github.com/nyu-devops-fall18/products.git  

# Go to folder that contains the Vagrantfile
cd products     

# To create the evironment needed for our services
vagrant up

# Connect to the virutalbox of our service using secure channel
vagrant ssh

# Go inside the virtual box 
cd /vagrant

# Start the services. To check it out, go to the browser and input the address: http://localhost:5000
honcho start

# Stop the service
<ctrl + c>

# To get out of the vagrant
exit

# To stop running the VM
vagrant halt
```

Try the following urls: <br>
e.g.1 to list all the products, please try link: http://localhost:5000/products <br>
e.g.2 to sort all the products by date, please try link: http://localhost:5000/products/latest <br>
e.g.3 to search a product by name, please try link: http://localhost:5000/products?name=desk <br>
e.g.4 to search a product by category, please try link: http://localhost:5000/products?category=clothing <br>

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
You can also directly visit our services on cloud: <br>
https://nyu-product-service-f18-prod.mybluemix.net/

# API Swagger Docs
The API documentation is on the following URL: <br>
https://nyu-product-service-f18-prod.mybluemix.net/apidocs/
