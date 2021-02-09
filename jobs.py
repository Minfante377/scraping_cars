import os
from utils.logger import logger
from helpers.ui_helper import UiHelper
from helpers import db_helper
from consts.consts import TrueCar


def truecar_job(brand, used):
    """
    Scrapes truecar.com using Selenium for a certain brand

    Args:
        - brand(str):
        - user(bool):

    Returs(None):

    """
    logger.log_info("Get driver for truecar job")
    driver_path = os.path.join(os.getcwd(), 'geckodriver')
    logger.log_info("Driver path is {}".format(driver_path))
    web_driver = UiHelper(driver_path, headless=False)

    logger.log_info("Get {}".format(TrueCar.URL))
    web_driver.get_url(TrueCar.URL)
    web_driver.wait_for_element(xpath='/html/body/div[2]/div[3]/main/div/'
                                      'div[2]/div[2]/section[2]/div/div[1]/h2')

    logger.log_info("Click on used")
    web_driver.click(partial_link_text='Used Cars')

    logger.log_info("Select brand {}".format(brand))
    web_driver.click(partial_link_text=brand)
    web_driver.wait_for_element(xpath='/html/body/div[2]/div[3]/main/div/'
                                      'div[4]/div/div/div/div[1]/div/h2/'
                                      'span[1]')
    if not used:
        logger.log_info("Select new cars")
        web_driver.click(partial_link_text='New Cars')

    logger.log_info("Enter ZIP code {}".format(TrueCar.ZIP_CODE))
    web_driver.click(xpath='/html/body/div[2]/div[3]/main/div/div/div[3]/div/'
                           'div[1]/div/div/div[1]/label[1]/div[2]/button')
    web_driver.implicit_wait(1)
    web_driver.send_focus(TrueCar.ZIP_CODE)
    web_driver.implicit_wait(5)

    logger.log_info("Start scraping")

    def scrape_page(brand, used):
        web_driver.implicit_wait(1)
        cars = web_driver.driver.find_elements_by_tag_name('a')
        car_class = 'linkable card card-1 card-shadow card-shadow-hover '\
                    'vehicle-card _1qd1muk'
        for car in cars:
            clas = car.get_attribute('class')
            if clas != car_class:
                continue
            url = car.get_attribute('href')
            logger.log_info("url is: {}".format(url))
            card_top = car.find_element_by_class_name('vehicle-card-top')
            spans = card_top.find_elements_by_tag_name('span')
            if len(spans) > 2:
                year = spans[1]
                model = spans[2]
            else:
                year = spans[0]
                model = spans[1]
            year = year.text
            model = model.text.replace(" ", "_")
            if used:
                miles = car.find_elements_by_css_selector('div.font-size-1.'
                                                          'text-truncate')
                miles = miles[2].text
                miles = miles.replace(',', '').replace('miles', '')
            else:
                miles = 0
            price = car.find_element_by_css_selector('div.heading-3.margin-y-1.'
                                                     'font-weight-bold').text
            price = price.replace(',', '').replace('$', '')
            is_new = 1 if not used else 0
            if not db_helper.check_car(model, is_new, year, price, miles):
                db_helper.add_car(brand, url, model, is_new, year, price, miles)

    while True:
        scrape_page(brand, used)
        try:
            logger.log_info("Go to the next page")
            web_driver.click(xpath='/html/body/div[2]/div[3]/main/div/div[3]/'
                                   'div/div[2]/div/div[2]/div[2]/nav/ul/'
                                   'li[14]/a')
            web_driver.implicit_wait(1)
        except Exception as e:
            logger.log_info("Out of pages")
            break
