# This file will have element selectors only for inventory page
selectors = {
    "all_inventory_items": "css=div.inventory_list > div.inventory_item",
    "button_item_add_to_cart": "css=button[data-test='add-to-cart-{placeholder}']",
    "button_item_remove": "css=button[data-test='remove-{placeholder}']",
    "label_item_price": "xpath=//button[@data-test='add-to-cart-{placeholder}']/preceding-sibling::div",
    'label_item_name': "xpath=//button[@data-test='add-to-cart-{placeholder}']/ancestor::div[@class='inventory_item_description']//div[@class='inventory_item_name']",
    'label_item_desc': "xpath=//button[@data-test='add-to-cart-{placeholder}']/ancestor::div[@class='inventory_item_description']//div[@class='inventory_item_desc']",
}
