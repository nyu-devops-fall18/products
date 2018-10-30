from app.model import Product
from datetime import datetime

def dbcreate():
    Product.logger.info(Product.query.with_entities(Product.id).all())
    if((Product.query.with_entities(Product.id).all()) != []):
        return
    Product(1, 'Desk', 'Wooden study desk', 'Furniture', 50, 'Boxed', 500, " ", 8).save()
    Product(2, 'Chair', 'Mesh office chair', 'Furniture', 30, 'Boxed', 1500, " ", 9).save()
    Product(3, 'Tshirt', 'Black printed tshirt', 'Clothing', 20, 'Boxed', 900, " ", 8).save()
    Product(4, 'Trousers', 'Brown linen trouser', 'Clothing', 35, 'Boxed', 300, " ", 10).save()
    Product(5, 'Mattress', 'Memory foam mattress', 'Furniture', 100, 'Boxed', 2000, " ", 7).save()
    Product.logger.info(Product.query.with_entities(Product.id).all())
# def dberase():
#     Product.query.delete()

