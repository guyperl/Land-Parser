from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from datetime import date

import time
import random


def main():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    global driver
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)


if __name__ == '__main__':
    main()
