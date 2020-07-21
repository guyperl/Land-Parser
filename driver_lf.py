from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from datetime import date

import time
import random


class LfListing:
    def __init__(self, address='', price=0, size=0):
        self.address = address
        self.price = price
        self.size = size

    def set_address(self, address=''):
        self.address = address

    def set_price(self, price=0):
        self.price = price

    def set_size(self, size=0):
        self.size = size

    def get_address(self):
        return self.address

    def get_price(self):
        return self.price

    def get_size(self):
        return self.size

    def __str__(self):
        return "Address: " + self.address + "\nPrice: $" + str(self.price) + "\nSize(acres): " + str(self.size)


def main():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    global driver
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)


if __name__ == '__main__':
    main()
