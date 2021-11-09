* Settings *
Documentation       This suite verifies End to End workflow for application. Covers sanity of most of the functionalities
Library             SeleniumLibrary
Library             Collections
Resource            Resources//LoginResources.txt
Resource            Resources//InventoryResources.txt
Resource            Resources//CartResources.txt
Resource            Resources//CheckoutResources.txt
Variables           VariableFiles//Items.py

Suite Setup         Open Browser with Login Page
Suite Teardown      Close Browser
Test Teardown       Run Keyword If Test Failed    Capture Page Screenshot

* Variables *
${username}     standard_user
${password}     secret_sauce
${first_name}   Test
${last_name}    User
${zip_code}     411017

* Test Cases *
End to End flow for application
    [Tags]    sanity    regression
    Login with "${username}" username and "${password}" password and verify successful login
    Verify item "${backpack}" is listed on inventory page
    Add item "${backpack}" to cart
    Navigate to cart page
    Verify item "${backpack}" with quantity "1" exists in cart
    User logs out from an application
    Login with "${username}" username and "${password}" password and verify successful login
    Navigate to cart page
    Verify item "${backpack}" with quantity "1" exists in cart
    Remove item "${backpack}" from cart
    Navigate to inventory page
    Add item "${backpack}" to cart
    Add item "${bikeLight}" to cart
    Navigate to cart page
    Navigate to checkout page
    Fill checkout information as firstname "${first_name}" lastname "${last_name}" and zipcode "${zip_code}"
    @{products}=            Create List                 ${backpack}     ${bikeLight}
    ${product_name}=        Get From Dictionary         ${backpack}     name
    ${product_name2}=       Get From Dictionary         ${bikeLight}    name
    &{quantities}=          Create Dictionary   ${product_name}    1    ${product_name2}    1
    Verify details on checkout overview page for item "${products}" and quantity "${quantities}"
    Complete checkout and verify successful checkout
    Navigate back to home from complete checkout page
    User logs out from an application

* Keywords *
Login with "${username}" username and "${password}" password and verify successful login
    User with name "${username}" and password "${password}" tries to log in into application
    Verify user logged in successfully