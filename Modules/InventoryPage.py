from PageObjectLibrary import PageObject
from Lib.webutil import webutil
from robot.utils import asserts
from robot.api import logger
import os
import builtins
import Messages
import sys

class InventoryPage(PageObject):
    webutil = webutil()
    selectors = webutil.get_selectors_from_obj_file("inventory.py")

    def __init__(self):
        PageObject.__init__(self)

    @webutil.log_args
    def check_product_listing(self, product):
        locator = self.selib.resolve_selector(self.selectors['button_item_add_to_cart'], product_name=product['name'])
        logger.info('Item Add to Cart Button Locator: %s' % locator)
        try:
            self.selib.element_should_be_visible(locator)
        except Exception as fault:
            logger.info('Error: %s' % str(fault))
            asserts.fail('Add to cart button is not displayed for %s product. i.e. Product is not listed on Invetory Page')
        finally:
            print("Done")


    @webutil.log_args
    def add_product_to_cart(self, product):
        print("Done")
        ## check product is displayed on inventory page





