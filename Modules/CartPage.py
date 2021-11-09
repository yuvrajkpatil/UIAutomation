# -*- coding: utf-8 -*-
from PageObjectLibrary import PageObject
from Lib.webutil import Webutil
from robot.utils import asserts
import Messages
from LoginPage import LoginPage

class CartPage(PageObject):
    # Create Webutil class object and load selectors from cart and common selector files
    webutil = Webutil()
    selectors = webutil.get_selectors_from_obj_file("cart.py")

    def __init__(self):
        PageObject.__init__(self)
        self.loginpage = LoginPage()

    def go_to_cart_page(self):
        """This method navigates user to cart page if not already on cart page"""
        # Get the current browser location
        current_location = self.selib.get_location()
        log.info('Current browser location: %s' % current_location)

        # Check if current location is same as baseurl
        if current_location == baseurl:
            # Current browser location is same as baseurl. i.e. user is not logged in. Login and verify login
            log.info('User is not logged in. Logging in as default user mentioned in webutil')
            self.loginpage.login(self.webutil.username, self.webutil.password)
            self.loginpage.verify_login()
        elif current_location != baseurl + Messages.CART_PAGE_URL:
            log.info('Navigating to cart page by clicking cart link')
            self.selib.click_element(self.selectors['link_cart'])
        else:
            log.info('User is already on cart page')

    def get_actual_item_details(self, locator):
        """This method gets actual item details displayed on cart page for given item locator.
        Returns item name, item description, item quantity, item price"""
        act_item_name = self.selib.get_text(
            self.webutil.resolve_selector(self.selectors['text_item_name'], locator))
        act_item_desc = self.selib.get_text(
            self.webutil.resolve_selector(self.selectors['text_item_desc'], locator))
        act_item_price = self.selib.get_text(
            self.webutil.resolve_selector(self.selectors['text_item_price'], locator))
        act_item_quantity = self.selib.get_text(
            self.webutil.resolve_selector(self.selectors['text_item_quantity'], locator))
        return act_item_name, act_item_desc, act_item_price, act_item_quantity


    @webutil.log_args
    def verify_item_in_cart(self, item, quantity='1', item_displayed=True):
        """
        This method verifies if given item is displayed on cart page.
        :param item: item details dictionary
        :param quantity: quantity to verify for item on cart page
        :param item_displayed: flag to check if item should be displayed on cart. True means should be displayed
        """
        if item_displayed:
            log.info('Verifying item %s should be displayed on cart page' % item['name'])
            locator = self.webutil.resolve_selector(self.selectors['button_item_remove'], item['locator'])
            # Checking if remove button for item with given name is available if not then failing the TC
            try:
                self.selib.element_should_be_visible(locator)
            except Exception as fault:
                log.info('Error occurred during remove button visibility check. Error: %s' % str(fault))
                asserts.fail(
                    'Remove button is not displayed for %s item. i.e. item is not added in Cart')
            finally:
                log.info('Remove Button for item is available, hence proceeding ahead with further verification')

                # Get actual item details and log them
                act_item_name, act_item_desc, act_item_price, act_item_quantity = self.get_actual_item_details(
                    item['locator'])
                exp_item_price = '$' + str(int(quantity) * item['price'])
                log.info('Item Name: Actual: %s, Expected: %s' % (act_item_name, item['name']))
                log.info('Item Description: Actual: %s, Expected: %s' % (act_item_desc, item['description']))
                log.info('Item Price: Actual: %s, Expected: %s' % (act_item_price, exp_item_price))
                log.info('Item Quantity: Actual: %s, Expected: %s' % (act_item_quantity, quantity))

                # Verify expected and actual item details are same
                assert_flag = act_item_desc == item['description'] and act_item_price == exp_item_price \
                              and act_item_name == item['name'] and act_item_quantity == quantity
                asserts.assert_true(assert_flag, 'Actual & Expected Values do not match.')
        else:
            log.info('Verifying item should not be displayed on cart page')
            locator = self.webutil.resolve_selector(self.selectors['button_item_remove'], item['locator'])
            self.selib.element_should_not_be_visible(locator)

    @webutil.log_args
    def remove_item_from_cart(self, item):
        """This method removes item from cart"""
        # Get remove button selector
        locator = self.webutil.resolve_selector(self.selectors['button_item_remove'], item['locator'])
        self.selib.click_button(locator)
        # Verify item is not displayed on cart page
        self.verify_item_in_cart(item, item_displayed=False)
