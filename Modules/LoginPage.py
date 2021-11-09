# -*- coding: utf-8 -*-
from PageObjectLibrary import PageObject
from Lib.webutil import Webutil
from robot.utils import asserts
import Messages

class LoginPage(PageObject):
    # Create Webutil class object and load selectors from login and common selector files
    webutil = Webutil()
    selectors = webutil.get_selectors_from_obj_file("login.py")

    # Mapping of short error to full error message
    error_messages = {
        'no_username': Messages.LOGIN_NO_USERNAME_ERROR,
        'no_password': Messages.LOGIN_NO_PASSWORD_ERROR,
        'invalid_credentials': Messages.LOGIN_INVALID_CREDS_ERROR,
        'locked_user': Messages.LOGIN_USER_LOCKED_ERROR
    }

    def __init__(self):
        PageObject.__init__(self)

    @webutil.log_args
    def open_login_page(self):
        """This method will set the required parameters and will open browser with baseurl"""
        log.info('Opening browser [%s] with URL [%s]' % (browser, baseurl))
        alias = 'chrome' if browser == 'gc' else 'firefox'
        self.selib.open_browser(baseurl, browser, alias=alias)

    @webutil.log_args
    def login(self, username, password):
        """This method tries to perform login"""
        # Reloading a login page
        self.selib.reload_page()
        current_url = self.selib.get_location()
        log.info('Current page URL: %s' % current_url)

        # Checking if current url and base url is same. If not logging out from application
        if baseurl == current_url:
            self.selib.wait_until_element_is_visible(self.selectors['input_username'])
        else:
            log.info('Login page is not opened. Looks like user is already logged in. Logging out from application')
            self.selib.click_element(self.selectors['button_burger_menu'])
            self.selib.click_link(self.selectors['link_logout'])

        if username:
            self.selib.input_text(self.selectors['input_username'], username)
        if password:
            self.selib.input_password(self.selectors['input_password'], password)
        self.selib.click_element(self.selectors['button_login'])

    @webutil.log_args
    def verify_login(self, success=True, exp_error=''):
        """
        This method verified user login. If successful checks PRODUCTS page title element is visible.
        IF failure login then verifies error message
        :param success: flag for successful or failed login. True is login successful else failed
        :param exp_error: expected error key. For supported values check self.error_messages dict keys
        """
        if success:
            log.info('Verifying successful user login')
            self.selib.wait_until_element_is_visible(self.selectors['label_page_title'], timeout=10)
            actual_header = self.selib.get_text(self.selectors['label_page_title'])
            log.info('Header: Actual: %s, Expected: %s' % (actual_header, Messages.INVENTORY_PAGE_HEADER))
            asserts.assert_true(actual_header == Messages.INVENTORY_PAGE_HEADER, 'Actual & Expected header do not match')
            log.info('User logged in successfully')
        elif not success and exp_error:
            log.info('Verifying failed user login')
            expected_message = self.error_messages.get(exp_error, '')
            log.info('Expected Error Message: %s' % expected_message)
            asserts.assert_true(expected_message, 'Invalid expected error key is given.')
            actual_message = self.selib.get_text(self.selectors['msg_login_failure'])
            log.info('Actual Error Message: %s' % actual_message)
            asserts.assert_equal(expected_message, actual_message, 'Expected and Actual error message do not match')
            log.info('Successfully verified user login failure')

    def logout(self):
        """This method does logout from an application"""
        # Get the current browser url
        current_location = self.selib.get_location()
        log.info('Current browser location: %s' % current_location)

        # User is logged in if current location is not same as baseurl and we need to do logout
        if current_location != baseurl:
            log.info('User is logged in. Logging out...')
            self.selib.click_element(self.selectors['button_burger_menu'])
            self.selib.wait_until_element_is_visible(self.selectors['link_logout'])
            self.selib.click_link(self.selectors['link_logout'])
            self.selib.element_should_be_enabled(self.selectors['input_username'])
        else:
            # User is already logged out
            log.info('User is already logged out')
