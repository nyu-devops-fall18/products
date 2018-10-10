from app.productmodel import Product

def dbcreate():
    if(list(Product.query.with_entities(Product.id).all()) != []):
        return
    else:
        Product(1,'Rose','Rose Sticks','Stem',20,'Boxed', 500, " ", 8).save()
        Product(2,'Rose Petals', 'Petals of Rose', 'Leaf', 30,'Boxed', 1500, " ", 9).save()
        Product(3,'Tulips', 'Tulip Sticks', 'Stem',40, 'Boxed', 900, " ", 8).save()
        Product(4,'Sunflower', 'Sunflower Sticks', 'Stem',50, 'Boxed', 300, " ", 10).save()
        Product(5,'Sunflower Petals', 'Petals of Sunflower', 'Leaf',25, 'Boxed', 2000, " ", 7).save()

# def dberase():
#     Product.query.delete()

