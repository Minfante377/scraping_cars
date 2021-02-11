class TrueCar:
    URL = 'https://truecar.com'
    ZIP_CODE = 90210


class AutoTrader:
    ZIP_CODE = 90210
    URL = 'https://www.autotrader.com/cars-for-sale/'\
          'all-cars?zip={}&makeCodeList='.format(ZIP_CODE)
