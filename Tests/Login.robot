* Settings *
Documentation       Login to test application
Library             SeleniumLibrary
Resource            Resources//LoginResources.txt

Suite Setup         Open Browser with Login Page
Suite Teardown      Close Browser
Test Template       Verify login functionality
Test Teardown       Run Keyword If Test Failed    Capture Page Screenshot

* Test Cases *                                                    Username                        Password          Expected_Error
TC01: Verify user logs in successfully with valid creds         standard_user                   secret_sauce        NA
    [Tags]    sanity    regression
TC02: Verify login error for locked out user                    locked_out_user                 secret_sauce        locked_user
    [Tags]    regression
TC03: Verify problem user logs in successfully                  problem_user                    secret_sauce        NA
    [Tags]    regression
TC04: Verify performance glitch user logs in successfully       performance_glitch_user         secret_sauce        NA
    [Tags]    regression
TC05: Verify user login fails with invalid creds                standard_user                   secret_sauce1       invalid_credentials
    [Tags]    sanity    regression
TC07: Verify error when user does not enter username            ${None}                         secret_sauce        no_username
    [Tags]    sanity    regression
TC08: Verify error when user does not enter password            standard_user                   ${None}             no_password
    [Tags]    sanity    regression


* Keywords *
Verify login functionality
    [Arguments]     ${username}     ${password}     ${error}
    User with name "${username}" and password "${password}" tries to log in into application
    Run Keyword If      '${error}'=='NA'     Verify user logged in successfully
    ...     ELSE    Verify error "${error}" for user login
