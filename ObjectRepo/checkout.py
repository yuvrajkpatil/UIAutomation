# This file will have element selectors only for checkout page
selectors = {
    "input_first_name": "css=[data-test='firstName']",
    "input_last_name": "css=[data-test='lastName']",
    "input_zip_code": "css=[data-test='postalCode']",
    "button_cancel": "css=[data-test='cancel']",
    "button_continue": "css=[data-test='continue']",
    "text_item_quantity": "xpath=//div[text()='{placeholder}']/ancestor::div[@class='cart_item']//div[@class='cart_quantity']",
    "text_item_name": "xpath=//div[text()='{placeholder}']/ancestor::div[@class='cart_item']//div[@class='inventory_item_name']",
    "text_item_desc": "xpath=//div[text()='{placeholder}']/ancestor::div[@class='cart_item']//div[@class='inventory_item_desc']",
    "text_item_price": "xpath=//div[text()='{placeholder}']/ancestor::div[@class='cart_item']//div[@class='inventory_item_price']",
    "label_payment_information": "xpath=//div[@class='summary_info']/div[text()='Payment Information:']",
    "text_payment_information": "xpath=//div[@class='summary_info']/div[text()='Payment Information:']/following-sibling::div[1]",
    "label_shipping_information": "xpath=//div[@class='summary_info']/div[text()='Shipping Information:']",
    "text_shipping_information": "xpath=//div[@class='summary_info']/div[text()='Shipping Information:']/following-sibling::div[1]",
    "label_item_sub_total": "css=div.summary_info .summary_subtotal_label",
    "label_item_tax": "css=div.summary_info .summary_tax_label",
    "label_item_total": "css=div.summary_info .summary_total_label",
    "button_finish": "css=[data-test='finish']",
    "button_back_home": "css=[data-test='back-to-products']",
    "text_thank_you": "css=h2.complete-header",
    "text_complete": "css=div.complete-text",
    "image_complete": "css=img.pony_express"
}
