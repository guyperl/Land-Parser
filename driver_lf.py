from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from datetime import date

import time
import random


class LfListing:
    def __init__(self, address='', price=0, size=0, link=''):
        self.address = address
        self.price = price
        self.size = size
        self.link = link

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

    def fits_parameters(self, price_low, price_high, size_low, size_high):
        return price_low <= self.price <= price_high and size_low <= self.size <= size_high

    def __str__(self):
        return "Address: " + self.address + "\nPrice: $" + str(self.price) + \
               "\nSize(acres): " + str(self.size) + \
               "\nLink: " + str(self.link) + "\n"


def get_parameters():
    location = input('Enter location: ')
    price_low = 0
    price_high = 0
    size_low = 0
    size_high = 0

    while True:
        price_low = input('Enter lowest price: ')
        if price_low.isnumeric():
            price_low = float(price_low)
            break
    while True:
        price_high = input('Enter highest price:')
        if price_high.isnumeric():
            if float(price_high) > price_low:
                price_high = float(price_high)
                break

    while True:
        size_low = input('Enter lowest size(in acres): ')
        if size_low.isnumeric():
            size_low = float(size_low)
            break
    while True:
        size_high = input('Enter highest size(in acres): ')
        if size_high.isnumeric():
            if float(size_high) > size_low:
                size_high = float(size_high)
                break

    return location, price_low, price_high, size_low, size_high


def find_listings_on_page(driver, listings, price_low, price_high, size_low, size_high):
    i = 0
    while True:
        listing = driver.find_elements_by_id('srch_listing_' + str(i))
        if len(listing) > 0:
            i += 1
            link = listing[0].find_elements_by_tag_name('a')[0].get_attribute('href')
            listing_text = listing[0].text.split('\n')
            if listing_text[0] == 'SIGNITURE' or listing_text[0] == 'PREMIUM':
                listing_text = listing_text[1:]
            current_listing = LfListing(address=listing_text[2],
                                        price=turn_numeric(listing_text[0]),
                                        size=turn_numeric(listing_text[1].split(' ')[0]),
                                        link=link)
            if current_listing.fits_parameters(price_low, price_high, size_low, size_high)
                listings.append(current_listing)
        else:
            break


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


def parse(driver, listings, price_low, price_high, size_low, size_high):
    pages = driver.find_elements_by_class_name('pagination')[0].find_elements_by_tag_name('li')
    for i in range(len(pages)):
        pages[i] = pages[i].find_elements_by_tag_name('a')[0].get_attribute('href')

    for i in range(len(pages)):
        print("Parsing page " + str(i + 1))
        time.sleep(5)
        if i == 1:
            detect_pop_up(driver)
        find_listings_on_page(driver, listings, price_low, price_high, size_low, size_high)
        if i != len(pages) - 1:
            driver.get(pages[i + 1])
        else:
            break


def detect_pop_up(driver):
    if len(driver.find_elements_by_class_name('save-search-modal')) != 0:
        driver.find_elements_by_class_name('saveSearchClose')[0].click()
        driver.refresh()


def write_results(filename, listings):
    print('Writing results to file...')
    with open(filename, 'w') as file:
        for listing in listings:
            file.write(listing + '\n')
    print('Results written')


def main():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    location, price_low, price_high, size_low, size_high = get_parameters()

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.get('https://landandfarm.com/search/TX/' + location + '-land-for-sale/')

    listings = []
    parse(driver, listings, price_low, price_high, size_low, size_high)

    output_listings(listings)
    write_results()


if __name__ == '__main__':
    main()
