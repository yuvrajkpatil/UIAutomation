# -*- coding: utf-8 -*-
from PageObjectLibrary import PageObject
from Lib.webutil import Webutil
from robot.utils import asserts
import Messages
from LoginPage import LoginPage

class CheckoutPage(PageObject):
    # Create Webutil class object and load selectors from checkout and common selector files
    webutil = Webutil()
    selectors = webutil.get_selectors_from_obj_file("checkout.py")

    def __init__(self):
        PageObject.__init__(self)
        self.loginpage = LoginPage()

    def go_to_checkout_page(self):
        """This method navigates user to checkout page if not already on checkout page"""
        # Get the current browser location
        current_location = self.selib.get_location()
        log.info('Current browser location: %s' % current_location)

        # Check if current location is same as baseurl
        if current_location == baseurl:
            # Current browser location is same as baseurl. i.e. user is not logged in. Login and verify login
            log.info('User is not logged in. Logging in as default user mentioned in webutil')
            self.loginpage.login(self.webutil.username, self.webutil.password)
            self.loginpage.verify_login()
        elif current_location != baseurl + Messages.CHECKOUT_PAGE_URL:
            log.info('Navigating to checkout page by clicking cart link and then checkout button')
            self.selib.click_element(self.selectors['link_cart'])
            self.selib.click_element(self.selectors['button_checkout'])
        else:
            log.info('User is already on checkout page')

    @webutil.log_args
    def fill_checkout_information(self, firstname, lastname, zipcode):
        """This method enters users information on checkout page. Like First Name, Last Name and Zip Code"""
        # Enter user information and click on Continue button
        self.selib.input_text(self.selectors['input_first_name'], firstname)
        self.selib.input_text(self.selectors['input_last_name'], lastname)
        self.selib.input_text(self.selectors['input_zip_code'], zipcode)
        self.selib.click_element(self.selectors['button_continue'])

        # Get the page header and verify its checkout overview page
        header = self.selib.get_text(self.selectors['label_page_title'])
        asserts.assert_true(header == Messages.CHECKOUT_OVERVIEW_PAGE_HEADER,
                            'Actual [%s] & Expected [%s] page header do not match' % (
                            header, Messages.CHECKOUT_OVERVIEW_PAGE_HEADER))

    def get_actual_item_details(self, pname):
        """This method gets actual item details displayed on checkout overview page for given item name.
        Returns item name, item description, item quantity, item price"""
        act_item_name = self.selib.get_text(
            self.webutil.resolve_selector(self.selectors['text_item_name'], pname))
        act_item_desc = self.selib.get_text(
            self.webutil.resolve_selector(self.selectors['text_item_desc'], pname))
        act_item_price = self.selib.get_text(
            self.webutil.resolve_selector(self.selectors['text_item_price'], pname))
        act_item_quantity = self.selib.get_text(
            self.webutil.resolve_selector(self.selectors['text_item_quantity'], pname))
        return act_item_name, act_item_desc, act_item_price, act_item_quantity


    def get_actual_order_details(self):
        """This method gets actual order details displayed on checkout overview page. Returns below actual details
        Payment Information Label, Payment Information value E.g. Card Details, Shipping Information Label,
        Shipping Information value, Item Total, Tax, Total
        """
        act_pay_info_label = self.selib.get_text(self.selectors['label_payment_information'])
        act_pay_info_text = self.selib.get_text(self.selectors['text_payment_information'])
        act_ship_info_label = self.selib.get_text(self.selectors['label_shipping_information'])
        act_ship_info_text = self.selib.get_text(self.selectors['text_shipping_information'])
        act_item_total = self.selib.get_text(self.selectors['label_item_sub_total'])
        act_tax = self.selib.get_text(self.selectors['label_item_tax'])
        act_total = self.selib.get_text(self.selectors['label_item_total'])
        return act_pay_info_label, act_pay_info_text, act_ship_info_label, act_ship_info_text, act_item_total, act_tax, act_total


    @webutil.log_args
    def verify_details_on_overview_page(self, items, quantities={}):
        """
        This method verifies items(s) displayed on checkout overview page along with other information
        :param items: list of items which are added for checkout. Each item will be a dictionary of item details
        :param quantities: dictionary with keys as item names and values as quantity
        """
        # Variable for calculating total items price
        item_total = 0
        # Verify item details for each item in items list
        for item in items:
            log.info('Verifying item details for %s item' % item['name'])
            # Get actual item details displayed on page
            act_item_name, act_item_desc, act_item_price, act_item_quantity = self.get_actual_item_details(
                item['name'])

            # Calculate item price based on number of quantity * single item price
            item_price = int(quantities[item['name']]) * item['price']
            item_total += item_price
            exp_item_price = "$" + str(item_price)
            log.info('Item Name: Actual: %s, Expected: %s' % (act_item_name, item['name']))
            log.info('Item Description: Actual: %s, Expected: %s' % (act_item_desc, item['description']))
            log.info('Item Price: Actual: %s, Expected: %s' % (act_item_price, exp_item_price))
            log.info('Item Quantity: Actual: %s, Expected: %s' % (act_item_quantity, quantities[item['name']]))

            # Verify expected and actual item details are same
            assert_flag = act_item_desc == item['description'] and act_item_price == exp_item_price and \
                          act_item_name == item['name'] and act_item_quantity == quantities[item['name']]
            asserts.assert_true(assert_flag, 'Actual & Expected Values do not match.')

        # Get actual order details
        act_pay_info_label, act_pay_info_val, act_ship_info_label, act_ship_info_val, act_item_total, \
        act_tax, act_total = self.get_actual_order_details()

        # Calculate expected item total, tax and total amount
        exp_item_total = 'Item total: $' + str(item_total)
        tax = (item_total * 8.03) / 100
        exp_tax = 'Tax: $%.2f' % (tax - 0.01)
        exp_total = 'Total: $%.2f' % (item_total + (tax - 0.01))

        # Log actual & expected order details
        log.info('Payment Info Label: Actual: %s, Expected: %s' % (act_pay_info_label, Messages.PAYMENT_INFO_LABEL))
        log.info('Payment Info Value: Actual: %s, Expected: %s' % (act_pay_info_val, Messages.PAYMENT_INFO_VALUE))
        log.info('Shipping Info Label: Actual: %s, Expected: %s' % (act_ship_info_label, Messages.SHIPPING_INFO_LABEL))
        log.info('Shipping Info Value: Actual: %s, Expected: %s' % (act_ship_info_val, Messages.SHIPPING_INFO_VALUE))
        log.info('Item Total: Actual: %s, Expected: %s' % (act_item_total, exp_item_total))
        log.info('Tax: Actual: %s, Expected: %s' % (act_tax, exp_tax))
        log.info('Total: Actual: %s, Expected: %s' % (act_total, exp_total))

        # Verify actual and expected order details are same
        assert_flag = act_pay_info_label == Messages.PAYMENT_INFO_LABEL and \
                      act_pay_info_val == Messages.PAYMENT_INFO_VALUE and \
                      act_ship_info_label == Messages.SHIPPING_INFO_LABEL and \
                      act_ship_info_val == Messages.SHIPPING_INFO_VALUE and \
                      act_item_total == exp_item_total and act_tax == exp_tax and act_total == exp_total
        asserts.assert_true(assert_flag, 'Actual & Expected Values do not match.')

    def complete_checkout_and_verify(self):
        """This method completes the checkout and verifies successful checkout"""
        # Complete checkout by clicking on finish
        log.info('Completing checkout by clicking on Finish button')
        self.selib.click_element(self.selectors['button_finish'])

        # Get page header and verify its same as checkout complete
        header = self.selib.get_text(self.selectors['label_page_title'])
        asserts.assert_true(header == Messages.CHECKOUT_COMPLETE_PAGE_HEADER,
                            'Actual [%s] & Expected [%s] page header do not match' % (
                            header, Messages.CHECKOUT_COMPLETE_PAGE_HEADER))

        # Get & log actual order complete texts
        act_thank_you_txt = self.selib.get_text(self.selectors['text_thank_you'])
        act_complete_txt = self.selib.get_text(self.selectors['text_complete'])
        log.info('Thank You Text: Actual: %s, Expected: %s' % (act_thank_you_txt, Messages.THANK_YOU_TEXT))
        log.info('Complete Text: Actual: %s, Expected: %s' % (act_complete_txt, Messages.COMPLETE_TEXT))

        # Verify actual and expected order complete tests are same
        assert_flag = act_thank_you_txt == Messages.THANK_YOU_TEXT and act_complete_txt == Messages.COMPLETE_TEXT
        asserts.assert_true(assert_flag, 'Actual & Expected order complete text do not match')
        # Verify Pony Express image is displayed on order complete page
        self.selib.element_should_be_visible(self.selectors['image_complete'])

    def navigate_to_home(self):
        """This method verifies Back Home button is displayed on order complete page
        And on clicking user user is redirected to inventory page"""
        # Verify Back Home button is available and on clicking it user is redirected to Inventory page
        self.selib.element_should_be_visible(self.selectors['button_back_home'])
        self.selib.click_element(self.selectors['button_back_home'])

        # Get page header and verify its same as inventory page header
        header = self.selib.get_text(self.selectors['label_page_title'])
        asserts.assert_true(header == Messages.INVENTORY_PAGE_HEADER,
                            'Actual [%s] & Expected [%s] page header do not match' % (
                            header, Messages.INVENTORY_PAGE_HEADER))
