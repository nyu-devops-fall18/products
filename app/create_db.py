from app.productmodel import Product

def dbcreate():
    Product(1,'Rose','Rose Sticks','Stem','Boxed', 500, " ", 8).save()
    Product(2,'Rose Petals', 'Petals of Rose', 'Leaf', 'Boxed', 1500, " ", 9).save()
    Product(3,'Tulips', 'Tulip Sticks', 'Stem', 'Boxed', 900, " ", 8).save()
    Product(4,'Sunflower', 'Sunflower Sticks', 'Stem', 'Boxed', 300, " ", 10).save()
    Product(5,'Sunflower Petals', 'Petals of Sunflower', 'Leaf', 'Boxed', 2000, " ", 7).save()