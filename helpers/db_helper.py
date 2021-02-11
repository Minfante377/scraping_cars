import sqlite3

from utils.logger import logger


def create_table():
    """
    Creates cars.db file and a new table called cars

    """
    db = sqlite3.connect("cars.db")
    cursor = db.cursor()
    logger.log_info("Creating database")
    query = """CREATE TABLE IF NOT EXISTS cars (
                    id INTEGER PRIMARY KEY,
                    url TEXT,
                    brand TEXT,
                    model TEXT,
                    is_new INTEGER,
                    year INTEGER,
                    miles INTEGER,
                    price INTEGER
               );"""
    cursor.execute(query)


def add_car(brand, url, model, is_new, year, price, miles=0):
    """
    Adds a new car to the cars table

    Args:
        - url(str):
        - model(str):
        - brand(str)
        - is_new(int): 1 for True, 0 for False.
        - year(int):
        - price(int)
        - miles(int)

    Returns(int):
        0 for success, 1 for failure.

    """
    logger.log_info("Adding a new car: ({}, {}, {}, {}, {})".format(model,
                                                                    is_new,
                                                                    year,
                                                                    miles,
                                                                    price))
    try:
        db = sqlite3.connect("cars.db")
        cursor = db.cursor()
        query = """INSERT INTO cars (url, brand, model, is_new, year, miles, price)
                   VALUES (?, ?, ?, ?, ?, ?, ?)"""

        cursor.execute(query, (url, brand, model, is_new, year, miles, price))
        db.commit()
        return 0
    except Exception as e:
        logger.log_error("Could not add car: {}".format(e))
        return 1


def check_car(model, is_new, year, price, miles=0):
    """
    Checks if a car exists.

    Args:
        - model(str)
        - is_new(int): 1 for True, 0 for False.
        - year(int):
        - price(int)
        - miles(int)

    Returns(bool):

    """
    logger.log_info("Checking if car ({}, {}, {}, {}, {}) exists".format(model,
                                                                         is_new,
                                                                         year,
                                                                         price,
                                                                         miles))
    db = sqlite3.connect("cars.db")
    cursor = db.cursor()
    query = """SELECT * FROM cars WHERE (
                   model="{}" AND
                   is_new={} AND
                   year={} AND
                   price={} AND
                   miles={});""".format(model, is_new, year, price, miles)
    cursor.execute(query)
    res = cursor.fetchone()
    logger.log_info("Results are: {}".format(res))
    if res:
        return True
    return False


def filter(brand=None, model=None, year=None, lower_price=None,
           higher_price=None):
    """
    Filter results by the non None parameters

    Args:
        - brand(str)
        - model(str):
        - year(str):
        - lower_price(int):
        - higher_price(int):

    Returns(list):
        list with the results

    """
    logger.log_info('Args are: {}, {}, {}, {}'.format(model, year, lower_price,
                                                      higher_price))
    db = sqlite3.connect("cars.db")
    cursor = db.cursor()
    query = """SELECT * FROM cars WHERE ("""
    if brand:
        query += 'brand="{}" AND '.format(brand)
    if model:
        query += 'model="{} AND " '.format(model)
    if year:
        query += 'year={} AND '.format(year)
    if lower_price:
        query += 'price > {} AND '.format(lower_price)
    if higher_price:
        query += 'price < {}'.format(higher_price)
    if query[-4:] == 'AND ':
        query = query[:-5]
    query += ');'

    logger.log_info("Executing query: {}".format(query))
    cursor.execute(query)
    res = cursor.fetchall()

    logger.log_info("Results are: {}".format(res))
    return res


def sort(brand=False, model=False, year=False, price=False):
    """
    Sort element by given parameter. Only one non False parameter is allowed.
    Args:
        - brand(bool):
        - model(bool):
        - year(bool):
        - price(bool):

    Returns(list):
        Sorted list.
    """
    if brand:
        sort_parameter = 'brand'
    elif model:
        sort_parameter = 'model'
    elif year:
        sort_parameter = 'year'
    elif price:
        sort_parameter = 'price'
    else:
        return None

    logger.log_info("Sorting by {}".format(sort_parameter))
    db = sqlite3.connect("cars.db")
    cursor = db.cursor()
    query = """SELECT * FROM cars ORDER BY {}""".format(sort_parameter)
    cursor.execute(query)
    res = cursor.fetchall()

    logger.log_info("Results are: {}".format(res))
    return res
