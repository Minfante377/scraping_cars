from flask import request, jsonify
from flask import Flask

from helpers import db_helper


api = Flask(__name__)


@api.route('/filter', methods=['GET'])
def filter():
   """
   Route is of the type /filter?model=x&year=x&lower_price=x&higher_price=x.
   Filter the results based on the parameters.
   """
   brand = request.args.get('brand')
   model = request.args.get('model')
   year = request.args.get('year')
   lower_price = request.args.get('lower_price')
   higher_price = request.args.get('higher_price')
   results = db_helper.filter(brand, model, year, lower_price, higher_price)
   return jsonify(results)


@api.route('/sort', methods=['GET'])
def sort():
    """
    Route is of the type /sort?model=True
    Sort the results based on one parameter
    """
    model = bool(request.args.get('model'))
    year = bool(request.args.get('year'))
    price = bool(request.args.get('price'))
    brand = bool(request.args.get('brand'))
    res = db_helper.sort(brand, model, year, price)
    return jsonify(res)
