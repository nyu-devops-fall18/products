from app.productmodel import Product
from datetime import datetime

def dbcreate():
    Product.logger.info(Product.query.with_entities(Product.id).all())
    if((Product.query.with_entities(Product.id).all()) != []):
        return
    Product(1,'Rose','Rose Sticks','Stem',20,'Boxed', 500, " ", 8, str(datetime.now()), 1).save()
    Product(2,'Rose Petals', 'Petals of Rose', 'Leaf', 30,'Boxed', 1500, " ", 9,str(datetime.now()), 1).save()
    Product(3,'Tulips', 'Tulip Sticks', 'Stem',40, 'Boxed', 900, " ", 8,str(datetime.now()), 1).save()
    Product(4,'Sunflower', 'Sunflower Sticks', 'Stem',50, 'Boxed', 300, " ", 10,str(datetime.now()), 1).save()
    Product(5,'Sunflower Petals', 'Petals of Sunflower', 'Leaf',25, 'Boxed', 2000, " ", 7,str(datetime.now()), 1).save()
    Product.logger.info(Product.query.with_entities(Product.id).all())
# def dberase():
#     Product.query.delete()

