# Land-Parser
Web scraper that finds lands/lots in specified locations. Can narrow down search given specific parameters such as price ranges or size ranges. Only works for Zillow.com. 

# Installation

Clone the repository using the https link provided.

```bash
git clone <link>
```

# Usage
Simply run the driver with python. Make sure the packages are installed before running the program. 

```bash
pip install <package>
```

Selenium, Webdriver_manager and smtplib must be installed in order for the driver to run. 

To run the program, run the following command in your command line.

```bash
python driver.py
```
To send the information inside of a file, run the following in the command line:

```bash
python Email.py
```
**Disclaimer:** The email only works with gmail accounts, all other accounts must be configured differently. Emails can be sent to emails other than gmail but login must be a gmail account. 
