from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

from utils.logger import logger


class UiHelper:

    def __init__(self, driver_path, headless=True):
        """
        Init Firefox webdriver

        Args:
            - driver_path(str): geckodriver full path.
            - headless(bool): add --headless option if True.

        """
        options = Options()
        if headless:
            options.add_argument("--headless")

        logger.log_info("Init webdriver")
        self.driver = webdriver.Firefox(options=options,
                                        executable_path=driver_path)

    def get_url(self, url):
        """
        Navigates to the given url

        Args:
            - url(str)

        """
        logger.log_info("Navigating to {}".format(url))
        self.driver.get(url)

    def get_element(self, class_name=None, xpath=None, _id=None, name=None,
                    link_text=None, partial_link_text=None, css_selector=None):
        """
        Try to find an element based on a parameter.

        Args:
            - class_name(str):
            - xpath(str):
            - _id(str):
            - name(str):
            - link_text(str):
            - partial_link_text(str):

        Returns(Selenium web object):

        """
        element = self._find_element(class_name, xpath, _id, name, link_text,
                                     partial_link_text, css_selector)
        return element

    def click(self, element=None, class_name=None, xpath=None, _id=None,
              name=None, link_text=None, partial_link_text=None,
              css_selector=None):
        """
        Clicks on a web element. Is the element is not provided, it tries to
        find it based on a parameter.

        Args:
            - element(selenium web object):
            - class_name(str):
            - xpath(str):
            - _id(str):
            - name(str):
            - link_text(str):
            - partial_link_text(str):

        Returns(Selenium web object):

        """
        if not element:
            element = self._find_element(class_name, xpath, _id, name, link_text,
                                         partial_link_text, css_selector)
        element.click()
        return element

    def send_keys(self, text, element=None, submit=False, class_name=None,
                  xpath=None, _id=None, name=None, link_text=None,
                  partial_link_text=None, css_selector=None):
        """
        Sends text to a web element. Is the element is not provided, it tries
        to find it based on a parameter.

        Args:
            - text(str): text to send.
            - element(selenium web object):
            - submit(bool): is true, sends ENTER after sending the text.
            - class_name(str):
            - xpath(str):
            - _id(str):
            - name(str):
            - link_text(str):
            - partial_link_text(str):

        Returns(Selenium web object):

        """
        if not element:
            element = self._find_element(class_name, xpath, _id, name, link_text,
                                         partial_link_text, css_selector)
        element.send_keys(text)
        if submit:
            element.submit()
        return element

    def get_text(self, element=None, class_name=None, xpath=None, _id=None,
                 name=None, link_text=None, partial_link_text=None,
                 css_selector=None):
        """
        Gets text from a web element. Is the element is not provided, it tries
        to find it based on a parameter.

        Args:
            - element(selenium web object):
            - class_name(str):
            - xpath(str):
            - _id(str):
            - name(str):
            - link_text(str):
            - partial_link_text(str):

        Returns(Selenium web object):

        """
        if not element:
            element = self._find_element(class_name, xpath, _id, name, link_text,
                                         partial_link_text, css_selector)
        return element.text

    def wait_for_element(self, timeout=10, class_name=None, xpath=None,
                         _id=None, name=None, link_text=None,
                         partial_link_text=None, css_selector=None):
        """
        Waits for an element to show.

        Args:
            - timeout(int): timeout in seconds
            - class_name(str):
            - xpath(str):
            - _id(str):
            - name(str):
            - link_text(str):
            - partial_link_text(str):

        Returns(tuple):
            (rc, element): rc is equal to 0 for success, -1 for error.

        """
        init = time.time()
        while time.time() - init < timeout:
            try:
                element = self._find_element(class_name, xpath, _id, name,
                                             link_text, partial_link_text,
                                             css_selector)
                return 0, element
            except Exception as e:
                logger.log_info("Element is not present."
                                "waiting 0.5s: {}".format(e))
                time.sleep(0.5)
        logger.log_error("Could not find element. Returning error")
        return -1, None

    def implicit_wait(self, delay):
        """
        Implicitly waits.

        Args:
            - delay(int): wait in seconds.

        """
        time.sleep(delay)

    def send_focus(self, text):
        """
        Send text to the focused element.

        Args:
            - text(str):

        """
        active_element = self.driver.switch_to.active_element
        active_element.send_keys(text)
        active_element.submit()

    def _find_element(self, class_name, xpath, _id, name, link_text,
                      partial_link_text, css_selector):
        if not class_name and not xpath and not _id and not name and \
                not link_text and not partial_link_text:
            logger.log_error("I cant find the element withouth info")
            return
        elif class_name:
            element = self.driver.find_element_by_class_name(class_name)
        elif xpath:
            element = self.driver.find_element_by_xpath(xpath)
        elif _id:
            element = self.driver.find_element_by_id(_id)
        elif name:
            element = self.driver.find_element_by_name(name)
        elif link_text:
            element = self.driver.find_element_by_link_text(link_text)
        elif css_selector:
            element = self.driver.find_element_by_css_selector(css_selector)
        else:
            element = self.driver.find_element_by_partial_link_text(partial_link_text)
        return element
