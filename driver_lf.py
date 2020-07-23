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
        return "Address: " + self.address + "\nPrice: $" + str(self.price) + "\nSize(acres): " + str(self.size) + '\n'


def get_parameters():
    location = input('Enter location: ')
    return location


def find_listings_on_page(driver, listings):
    i = 0
    while True:
        listing = driver.find_elements_by_id('srch_listing_' + str(i))
        if len(listing) > 0:
            i += 1
            listings.append(listing[0])
        else:
            break


def parse_listings(listings):
    parsed_listings = []
    for listing in listings:
        listing_text = listing.text.split('\n')
        print(listing_text)
        if listing_text[0] == 'SIGNITURE' or listing_text[0] == 'PREMIUM':
            listing_text = listing_text[1:]
        current_listing = LfListing(address=listing_text[2],
                                    price=turn_numeric(listing_text[0]),
                                    size=turn_numeric(listing_text[1].split(' ')[0]))
        parsed_listings.append(current_listing)
    return parsed_listings


def turn_numeric(string):
    return_string = ''

    for i in range(len(string)):
        if string[i].isnumeric() or string[i] == '.':
            return_string += string[i]

    if return_string == '':
        return 0

    return float(return_string)


def output_listings(listings):
    for listing in listings:
        print(listing)


def main():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    location = get_parameters()

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.get('https://landandfarm.com/search/TX/' + location + '-land-for-sale/')

    listings = []
    find_listings_on_page(driver, listings)

    listings = parse_listings(listings)
    output_listings(listings)


if __name__ == '__main__':
    main()
