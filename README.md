# Land-Parser
Web scraper that finds lands/lots in specified locations. Can narrow down search given specific parameters such as price ranges or size ranges. Only works for Zillow.com and landandfarm.com. 

# Installation

Clone the repository using the https link provided.

```bash
git clone https://github.com/iamjeffx/Land-Parser.git
```
Make sure that the required python packages are installed. This can be done using pip:
```bash
pip install selenium
pip install webdriver-manager
pip install smtplib
```

# Usage
Simply run the driver with python. Make sure the packages are installed before running the program. 

To run the scraper that uses Zillow, run the following command in your command line.

```bash
python driver.py
```
Be careful when running the Zillow driver, Zillow has code to prevent massive scrapes of data in a specific time frame, therefore sometimes you may be met with an error page telling you to verify that you are human(this is what the detect_error_page function is for). Currently, the most efficient method is just to complete the puzzle and try running the code again(I know, not very convenient). You can also mess around with the delays between each scrape cycle to prevent this although if this script is run enough times within a day, the error page is bound to pop up. 

To run the scraper that uses landandfarm, run the following command:

```bash
python driver_lf.py
```
Default state for landandfarm is Texas but the state can be changed by changing the **url** by changing the second token in the url.

To send the information inside of a file, run the following in the command line:

```bash
python Email.py
```
**Disclaimer:** The email only works with gmail accounts, all other accounts must be configured differently. Emails can be sent to emails other than gmail but login must be a gmail account. 
