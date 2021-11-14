# RobotFramework-Python3-SeleniumLibrary- Web UI Automation.

![alt text](https://raw.githubusercontent.com/yuvrajkpatil/UIAutomation/main/images/banner.png)

Tested on:
------------------
Used Web App: https://www.saucedemo.com/

Robot Framework 4.1.2 (Python 3.10.0 on win64)

Python 3.10.0

SeleniumLibrary 5.1.3

PageObjectLibrary 1.1

Selenium 4.0.0

Required installations:
--------------------
Install python3 from following website for your machine architecture.

Python 3 -> https://www.python.org/downloads/

Install required dependencies using pip once python is installed.

Checkout the repository and navigate to base repository folder and then run below command.

pip install -r requirements.txt

Running Tests Commands:
----------------------
Go to base checkout directory and run below commands:

1. Set PATH:

set PATH=C:\Windows\system32;%SystemRoot%\system32;%SystemRoot%;%SystemRoot%\System32\Wbem;C:\<python_install_dir>;C:\<python_install_dir>\Scripts;

2. set PYTHONPATH:

set PYTHONPATH=C:\<python_install_dir>;C:\<python_install_dir>\Scripts;C:\<python_install_dir>\Lib;C:\<python_install_dir>\Lib\site-packages;D:\<repo_checkout_dir>\Modules;

These paths are for Windows machine, you can run respective commands for other platforms.

3. Execute all test suites under Tests directory
    python testrunner.py -t Tests\ -b <gc/ff>

4. To execute test cases with specific tag: Below command will execute only test cases which are tagged as sanity
    python testrunner.py -t Tests\ -b <gc/ff> -i sanity

5. To execute test cases with multiple tags: Below command will execute test cases which are tagged as either sanity, regression or both
    python testrunner.py -t Tests\ -b <gc/ff> -i sanity,regression

![alt text](https://raw.githubusercontent.com/yuvrajkpatil/UIAutomation/main/images/console_output.png)

![alt text](https://raw.githubusercontent.com/yuvrajkpatil/UIAutomation/main/images/html_report.png)


Extra Information/Libraries/Updates/Documentations/Tools:
-------------------------------------------------------

https://robotframework.org/
