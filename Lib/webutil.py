from PageObjectLibrary import PageObject
import os
from robot.api import logger
import builtins

# Create Logger class
class QAlogger():
    def info(self, msg):
        logger.info(msg, also_console=True)

    def debug(self, msg):
        logger.debug(msg)

    def error(self, msg):
        logger.debug(msg)

    def traceback(self, arg):
        logger.debug(arg)

    def critical(self, msg):
        logger.debug(msg)


class Webutil(PageObject):
    selectors = {}

    def __init__(self):
        PageObject.__init__(self)
        self.username = 'standard_user'
        self.password = 'secret_sauce'
        builtins.log = QAlogger()
        if not self.selectors:
            obj_selectors = self.get_selectors_from_obj_file()
            self.selectors.update(obj_selectors)

    def log_args(self, func):
        """
        Function to log all arguments of decorated function
        """
        def wrapper(*func_args, **func_kwargs):
            arg_names = func.__code__.co_varnames[:func.__code__.co_argcount]
            args = func_args[:len(arg_names)]
            defaults = func.__defaults__ or ()
            args = args + defaults[len(defaults) - (func.__code__.co_argcount - len(args)):]
            params = zip(arg_names, args)
            new_arg_list = [list(i) for i in params]
            for key in func_kwargs:
                for param in new_arg_list:
                    if key == param[0]:
                        param[1] = func_kwargs[key]
            new_arg_list = [tuple(i) for i in new_arg_list]
            logger.info(func.__name__ + ' (' + ', '.join('%s = %r' % p for p in new_arg_list) + ' )')
            return func(*func_args, **func_kwargs)
        return wrapper

    def get_selectors_from_obj_file(self, filename=''):
        """
        This method loads selectors from given file and common.py selector file into self.selectors dictionary
        :param filename: page specific selector filename which selectors needs to be added into self.selectors dict
        :return: selector dictionary
        """
        log.info('Loading selectors from file')
        if filename:
            try:
                objfile = open(os.path.join('ObjectRepo', filename), "U").read()
            except Exception as fault:
                print("Failed to get selectors file '%s'. Error: %s" % (filename, str(fault)))

            # Load selectors from file into temporary dictionary
            page_dict = {}
            exec(objfile, page_dict)
            # Add page selectors into selectors dict
            selectors = page_dict['selectors']
        else:
            selectors = self.selectors

        # Load selectors from common.py file into selectors dictionary
        try:
            commobj = open(os.path.join("ObjectRepo", "common.py"), "U").read()
        except Exception as fault:
            logger.info("Failed to get common object locator file'. Error: %s" % str(fault))
        comm_obj = {}
        exec(commobj, comm_obj)
        comm_selectors = comm_obj['selectors']
        # Add common selectors to page selectors
        selectors.update(comm_selectors)
        return selectors

    def resolve_selector(self, selector, value):
        """
        This method replaces the placeholder in selector with actual value
        :param selector: selector string with placeholder
        :param value: value which needs to be replaced at placeholder
        :return: selector with value inplace of placeholder
        """
        log.info('Selector with placeholder: %s, value: %s' % (selector, value))
        locator = selector.replace('{placeholder}', value)
        log.info('Resolved Selector: %s' % locator)
        return locator

