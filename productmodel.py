from sqlalchemy import create_engine

engine = create_engine("product.db")

class ValidationError (ValueError):
    pass

class Product(object):

    product_data = []
    index = 0
    def __init__(self, product_id=0, pname='', pcategory=''):
        """ Initialize a Pet """
        self.id = product_id
        self.name = pname
        self.category = pcategory

    def save(self):
        # if(self.id == 0):
        #     self.id = self.id
        #     Product.product_data.append(self)
        # else:
        for i in range(len(Product.product_data)):
            if(Product.product_data[i].id == self.id):
                Product.product_data[i] = self
                break

    def delete(self):
        Product.product_data.remove(self)

    def serialize(self):
        return {"id": self.id, "name": self.name, "category":self.category}

    def deserialize(self, productdata):
        if not isinstance(productdata, dict):
            raise ValidationError('Invalid product: body of request contained bad or no data')
        try:
            self.name = productdata['name']
            self.category = productdata['category']
        except KeyError as err:
            raise ValidationError('Invalid product: missing ' + err.args[0])
        return
