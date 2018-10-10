from flask import Flask, jsonify, request, make_response
from flask_api import status

from flask_sqlalchemy import SQLAlchemy
from productmodel import Product

app = Flask("__name__")

@app.route("/")
def index():
    return 'Hello Flask!'


# LIST ALL FLOWERS
@app.route('/flowers', methods=['GET'])
def list_flowers()
     """ Return all the flowers"""
     flowers = []
     name = request.args.get('name')
     category = request.args.get('category')
     if name:
         flowers = Flower.find_by_name(name)
     elif category:
         flowers = Flower.find_by_category(category)
     else:
         flowers = Flower.all()
     results = [flower.serialize() for flower in flowers]
     return make_response(jsonify(results), status.HTTP_200_OK)


if __name__ == "__main__":
    app.run(debug=True)


