from PageObjectLibrary import PageObject
from Lib.webutil import Webutil
from robot.utils import asserts
import Messages
from LoginPage import LoginPage

class InventoryPage(PageObject):
    # Create Webutil class object and load selectors from inventory and common selector files
    webutil = Webutil()
    selectors = webutil.get_selectors_from_obj_file("inventory.py")

    def __init__(self):
        PageObject.__init__(self)
        self.loginpage = LoginPage()

    def go_to_inventory_page(self):
        """This method navigates user to inventory page if not already on inventory page"""
        # Get the current browser location
        current_location = self.selib.get_location()
        log.info('Current browser location: %s' % current_location)

        # Check if current location is same as baseurl
        if current_location == baseurl:
            # Current browser location is same as baseurl. i.e. user is not logged in. Login and verify login
            log.info('User is not logged in. Logging in as default user mentioned in webutil')
            self.loginpage.login(self.webutil.username, self.webutil.password)
            self.loginpage.verify_login()
        elif current_location != baseurl + Messages.INVENTORY_PAGE_URL:
            log.info('Navigating to inventory page by clicking burger menu and then all items link')
            self.selib.click_element(self.selectors['button_burger_menu'])
            self.selib.click_link(self.selectors['link_all_items'])
        else:
            log.info('User is already on inventory page')

    def get_actual_item_details(self, locator):
        """This method gets the actual item details shown on inventory page"""
        act_item_name = self.selib.get_text(self.webutil.resolve_selector(self.selectors['label_item_name'], locator))
        act_item_desc = self.selib.get_text(self.webutil.resolve_selector(self.selectors['label_item_desc'], locator))
        act_item_price = self.selib.get_text(self.webutil.resolve_selector(self.selectors['label_item_price'], locator))
        return act_item_name, act_item_desc, act_item_price

    @webutil.log_args
    def check_item_listing(self, item):
        """This method check given item is displayed on inventory page.
        First checks if Add to Cart button is available for item. If yes then checks all other item details.
        If button is not available then logs the error and fails TC"""
        self.go_to_inventory_page()
        locator = self.webutil.resolve_selector(self.selectors['button_item_add_to_cart'], item['locator'])
        # Checking if Add to Cart button for item with given name is available if not then failing the TC
        try:
            self.selib.element_should_be_visible(locator)
        except Exception as fault:
            log.info('Error occurred during Add to Cart button visibility check. Error: %s' % str(fault))
            asserts.fail(
                'Add to cart button is not displayed for %s item. Hence item is not listed on Inventory Page')
        finally:
            log.info('Add to Cart Button for item is available, hence proceeding ahead with further verification')

            # Get actual item details and log them
            act_item_name, act_item_desc, act_item_price = self.get_actual_item_details(item['locator'])
            exp_item_price = '$' + str(item['price'])
            log.info('Item Name: Actual: %s, Expected: %s' % (act_item_name, item['name']))
            log.info('Item Description: Actual: %s, Expected: %s' % (act_item_desc, item['description']))
            log.info('Item Price: Actual: %s, Expected: %s' % (act_item_price, exp_item_price))

            # Verify expected and actual item details are same
            assert_flag = act_item_desc == item['description'] and act_item_price == exp_item_price \
                          and act_item_name == item['name']
            asserts.assert_true(assert_flag, 'Actual & Expected Values do not match.')

    @webutil.log_args
    def add_item_to_cart(self, item):
        """This method adds given item into cart"""
        self.go_to_inventory_page()
        # Click Add to cart button and verify Remove button is available for same item
        self.selib.click_button(
            self.webutil.resolve_selector(self.selectors['button_item_add_to_cart'], item['locator']))
        self.selib.element_should_be_visible(
            self.webutil.resolve_selector(self.selectors['button_item_remove'], item['locator']))







