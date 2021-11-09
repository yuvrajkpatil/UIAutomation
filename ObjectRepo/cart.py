# This file will have element selectors only for cart page

selectors = {
    "button_continue_shopping": "css=[data-test='continue-shopping']",
    "button_item_remove": "css=[data-test='remove-{placeholder}']",
    "text_item_quantity": "xpath=//button[@data-test='remove-{placeholder}']/ancestor::div[@class='cart_item']/div[@class='cart_quantity']",
    "text_item_price": "xpath=//button[@data-test='remove-{placeholder}']/ancestor::div[@class='cart_item']//div[@class='inventory_item_price']",
    "text_item_desc": "xpath=//button[@data-test='remove-{placeholder}']/ancestor::div[@class='cart_item']//div[@class='inventory_item_desc']",
    "text_item_name": "xpath=//button[@data-test='remove-{placeholder}']/ancestor::div[@class='cart_item']//div[@class='inventory_item_name']"
}
