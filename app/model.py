import logging
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime
import ibm_db


db = SQLAlchemy()

class ValidationError (ValueError):
    pass

class Product(db.Model):

    logger = logging.getLogger(__name__)
    app = None

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63))
    description = db.Column(db.String(511))
    category = db.Column(db.String(63))
    price = db.Column(db.Integer)
    condition = db.Column(db.String(63))
    inventory = db.Column(db.Integer)
    review = db.Column(db.String(511))
    rating = db.Column(db.Integer)
    updateddate = db.Column(db.String(63))
    updateCount = db.Column(db.Integer)
    totalrating = db.Column(db.Integer)

    def __init__(self,pid,pname,pdesc,pcat,pprice,pcond,pinv,prev,prat):
        self.id = pid
        self.name = pname
        self.description = pdesc
        self.category = pcat
        self.price = pprice
        self.condition = pcond
        self.inventory = pinv
        self.review = prev
        self.rating = prat
        self.updateddate = str(datetime.now())
        self.updateCount = 1
        self.totalrating = prat

    def __repr__(self):
        return '<Product %r>' % (self.name)

    def save(self):
        templist = list(Product.query.with_entities(Product.id).all())
        idlist = []
        for i in templist:
            idlist.append(i[0])
        if not self.id:
            db.session.add(self)
        elif self.id in idlist:
            lastproduct = Product.query.order_by(Product.id.desc()).first()
            self.id = lastproduct.id + 1
            db.session.add(self)
        else:
            db.session.add(self)
        db.session.commit()

    def update(self):
        self.updateCount+=1
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        return {"id": self.id, "name": self.name, "description":self.description, "category": self.category, "price" : self.price,
                "condition" : self.condition, "inventory": self.inventory, "review": self.review, "rating": self.rating, "updatedDate" : self.updateddate}

    def deserialize(self, productdata):
        if not isinstance(productdata, dict):
            raise ValidationError('Invalid product: body of request contained bad or no data')
        try:
            self.name = productdata['name']
            self.description = productdata['description']
            self.category = productdata['category']
            self.price = productdata['price']
            self.condition = productdata['condition']
            self.inventory = productdata['inventory']
            self.review = productdata['review']
            self.rating = productdata['rating']
            self.updateddate = str(datetime.now())
            self.totalrating += int(productdata['rating'])
        except KeyError as err:
            raise ValidationError('Invalid product: missing ' + err.args[0])
        return self

    @staticmethod
    def init_db(app):
        """ Initializes the database session """
        Product.logger.info('Initializing database')
        Product.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @staticmethod
    def search_by_price(minimum, maximum):
        Product.logger.info("Searching for all products within the price range of minimum to maximum")
        return Product.query.filter((Product.price.between(minimum,maximum)))

    @staticmethod
    def delete_all():
        Product.logger.info("Deleting all products")
        db.session.query(Product).delete()
        db.session.commit()

    @staticmethod
    def all():
        """ Returns all of the products in the database """
        Product.logger.info('Processing all Products')
        # print(Product.query.all())
        return Product.query.all()

    @staticmethod
    def find_by_name(name):
        Product.logger.info('Processing by name = %s', name)
        return Product.query.filter(func.lower(Product.name) == func.lower(name))

    @staticmethod
    def find_by_category(category):
        Product.logger.info('Processing by category = %s', category)
        return Product.query.filter(func.lower(Product.category) == func.lower(category))

    @staticmethod
    def find_by_id(product_id):
        Product.logger.info("Finding a product")
        return Product.query.get(product_id)

    @staticmethod
    def sort_by_date():
        Product.logger.info("Return all products by updated date")
        # Product.logger.info(Product.query.order_by(Product.updateddate.desc()))
        return Product.query.order_by(Product.updateddate.desc())
