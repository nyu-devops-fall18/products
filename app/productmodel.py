import logging
from flask_sqlalchemy import SQLAlchemy

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
        # else:
        #     db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.remove(self)
        db.session.commit()

    def serialize(self):
        return {"name": self.name, "description":self.description, "category": self.category, "price" : self.price,
                "condition" : self.condition, "inventory": self.inventory, "review": self.review, "rating": self.rating}

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
