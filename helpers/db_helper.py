import sqlite3

from utils import logger


def create_table():
    """
    Creates cars.db file and a new table called cars

    """
    db = sqlite3.connect("cars.db")
    cursor = db.cursor()
    logger.log_info("Creating database")
    query = """CREATE TABLE IF NOT EXISTS cars (
                    id INTEGER PRIMARY KEY,
                    brand TEXT NOT NULL,
                    is_new INTEGER,
                    year INTEGER,
                    miles INTEGER,
                    price INTEGER,
               );"""
    cursor.execute(query)


def add_car(brand, is_new, year, price, miles=0):
    """
    Adds a new car to the cars table

    Args:
        - brand(str)
        - is_new(int): 1 for True, 0 for False.
        - year(int):
        - price(int)
        - miles(int)

    Returns(int):
        0 for success, 1 for failure.

    """
    logger.log_info("Adding a new car: ({}, {}, {}, {}, {})".format(brand,
                                                                    is_new,
                                                                    year,
                                                                    miles,
                                                                    price))
    try:
        db = sqlite3.connect("cars.db")
        cursor = db.cursor()
        query = """INSERT INTO cars (brand, is_new, year, miles, price)
                   VALUES (?, ?, ?, ?, ?)"""

        cursor.execute(query, (brand, is_new, year, miles, price))
        db.commit()
        return 0
    except Exception as e:
        logger.log_error("Could not add car: {}".format(e))
        return 1


def check_car(brand, is_new, year, price, miles=0):
    """
    Checks if a car exists.

    Args:
        - brand(str)
        - is_new(int): 1 for True, 0 for False.
        - year(int):
        - price(int)
        - miles(int)

    Returns(bool):

    """
    logger.log_info("Checking if car ({}, {}, {}, {}, {}) exists".format(brand,
                                                                         is_new,
                                                                         year,
                                                                         price,
                                                                         miles))
    db = sqlite3.connect("cars.db")
    cursor = db.cursor()
    query = """SELECT * FROM cars WHERE (
                   brand={},
                   is_new={},
                   year={},
                   price={},
                   miles={}
               );""".format(brand, is_new, year, price, miles)
    cursor.execute(query)
    res = cursor.fetchall()
    logger.log_info("Results are: {}".format(res))
    if res:
        return True
    return False
