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
    condition = db.Column(db.String(63))
    inventory = db.Column(db.Integer)
    review = db.Column(db.String(511))
    rating = db.Column(db.Integer)

    def __init__(self,pid,pname,pdesc,pcat,pcond,pinv,prev,prat):
        self.id = pid
        self.name = pname
        self.description = pdesc
        self.category = pcat
        self.condition = pcond
        self.inventory = pinv
        self.review = prev
        self.rating = prat

    def __repr__(self):
        return '<Product %r>'.format(self.name)

    def save(self):
        # if not self.id:
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.remove(self)
        db.session.commit()

    def serialize(self):
        return {"id": self.id, "name": self.name, "description":self.description, "category": self.category,
                "condition" : self.condition, "inventory": self.inventory, "review": self.review, "rating": self.review}

    def deserialize(self, productdata):
        if not isinstance(productdata, dict):
            raise ValidationError('Invalid product: body of request contained bad or no data')
        try:
            self.name = productdata['name']
            self.description = productdata['description']
            self.category = productdata['category']
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
