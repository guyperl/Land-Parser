from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from datetime import date

import time
import random


class LandListing:
    def __init__(self, price=0, link='', size=0, address=''):
        self.price = price
        self.link = link
        self.size = size
        self.address = address

    def get_price(self):
        return self.price

    def get_link(self):
        return self.link

    def get_size(self):
        return self.size

    def get_address(self):
        return self.address

    def set_price(self, price=0):
        self.price = price

    def set_link(self, link=''):
        self.link = link

    def set_size(self, size=0):
        self.size = size

    def set_address(self, address=''):
        self.address = address

    def price_in_range(self, low, high):
        return low <= self.get_price() <= high

    def size_in_range(self, low, high):
        return low <= self.get_size() <= high

    def listing_in_range(self, price_low, price_high, size_low, size_high):
        return self.price_in_range(price_low, price_high) and self.size_in_range(size_low, size_high)

    def __str__(self):
        string = "Address: " + self.get_address() + "\n"
        string += "Size: " + str(self.get_size()) + "\n"
        string += "Price: " + str(self.get_price()) + "\n"
        string += "Link: " + self.get_link() + "\n"
        return string


def is_multiple_of_4(num):
    return num % 4 == 0


def turn_numeric(string):
    return_string = ''

    for i in range(len(string)):
        if string[i].isnumeric():
            return_string += string[i]

    if return_string == '':
        return 0

    return int(return_string)


def parse_listing_price(listing):
    price = listing.find_element_by_class_name("list-card-price").text
    price = turn_numeric(price)
    return price


def parse_listing_address(listing):
    return listing.find_element_by_class_name("list-card-addr").text


def parse_listing_size(listing):
    size = listing.find_element_by_class_name("list-card-details").text
    size = turn_numeric(size)
    return size


def parse_listing_link(listing):
    return listing.find_element_by_class_name("list-card-info").find_element_by_tag_name("a").get_attribute("href")


def parse_listing(listing):
    price = parse_listing_price(listing)
    address = parse_listing_address(listing)
    link = parse_listing_link(listing)
    size = parse_listing_size(listing)
    return LandListing(price=price, address=address, size=size, link=link)


def output_list(elements):
    for item in elements:
        print(item)


def parse(browser, good_listings, page_number, price_low, price_high, size_low, size_high, filename):
    reset_file(filename)

    while True:
        print('Parsing Page ' + str(page_number))
        listings = browser.find_elements_by_class_name("list-card")

        for listing in listings:
            current_listing = parse_listing(listing)
            if current_listing.listing_in_range(price_low, price_high, size_low, size_high):
                good_listings.append(current_listing)
                write_element_to_file(filename, current_listing)
                print(current_listing.__str__() + '\n')

        next_page_button = browser.find_elements_by_class_name('PaginationButton-si2hz6-0')

        try:
            next_page_button[4].click()
        except:
            break

        if detect_error_page(browser):
            print('ERROR PAGE DETECTED: CLOSING BROWSER')
            break

        if is_multiple_of_4(page_number):
            time.sleep(random.uniform(20, 25))
        else:
            time.sleep(15)
        page_number += 1


def set_to_lands_and_lots(browser):
    home_type_button = browser.find_elements_by_class_name('home-type')[0]
    home_type_button.click()

    browser.find_elements_by_id('home-type_isSingleFamily')[0].click()
    browser.find_elements_by_id('home-type_isManufactured')[0].click()
    browser.find_elements_by_id('home-type_isCondo')[0].click()
    browser.find_elements_by_id('home-type_isMultiFamily')[0].click()
    browser.find_elements_by_id('home-type_isApartment')[0].click()
    browser.find_elements_by_id('home-type_isTownhouse')[0].click()

    time.sleep(15)


def reset_file(filename):
    with open(filename, 'w') as file:
        file.write('')


def write_element_to_file(filename, element):
    with open(filename, 'a') as file:
        file.write(element.__str__())
        file.write('\n')


def detect_error_page(browser):
    if len(browser.find_elements_by_class_name('error-content-block')) != 0:
        return True
    return False


def get_parameters():
    price_low = 0
    price_high = 0
    size_low = 0
    size_high = 0

    while True:
        price_low = input('Input lowest price: ')
        if price_low.isnumeric():
            price_low = float(price_low)
            break

    while True:
        price_high = input('Input highest price: ')
        if price_high.isnumeric():
            price_high = float(price_high)
            break

    while True:
        size_low = input('Input lowest size(acres): ')
        if size_low.isnumeric():
            size_low = float(size_low)
            break

    while True:
        size_high = input('Input highest size(acres): ')
        if size_high.isnumeric():
            size_high = float(size_high)
            break

    location = input('Input location: ').strip().replace(' ', '-')

    return price_low, price_high, size_low, size_high, location


def construct_filename(location, price_low, price_high, size_low, size_high):
    return location + '_results_' + str(date.today()) + \
           str(price_low) + '_' + str(price_high) + '_' + \
           str(size_low) + '_' + str(size_high)


def click_price(browser, price_low, price_high):
    price_button = browser.find_elements_by_class_name("price")
    if len(price_button) != 0:
        price_button = price_button[0]
    else:
        return
    price_button.click()

    time.sleep(5)

    browser.find_elements_by_id('price-exposed-min')[0].click()
    browser.find_elements_by_id('price-exposed-min')[0].send_keys(str(price_low))
    browser.find_elements_by_id('price-exposed-max')[0].click()
    browser.find_elements_by_id('price-exposed-max')[0].send_keys(str(price_high))

    browser.find_elements_by_class_name('home-type')[0].click()

    time.sleep(5)

    browser.refresh()


def main():
    price_low, price_high, size_low, size_high, location = get_parameters()
    filename = construct_filename(location, price_low, price_high, size_low, size_high)

    page_number = 1

    good_listings = []

    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    global driver
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.get("https://zillow.com/homes/" + location + "_rb/")

    if detect_error_page(driver):
        print('ERROR PAGE DETECTED')
        while True:
            close = input('Would you like to close the browser(y/n)? ')
            close = close.lower()
            if close == 'y' or close == 'yes':
                driver.close()
                break
            elif close == 'n' or close == 'no':
                break
            else:
                print('The input you provided is not valid.')
    else:
        set_to_lands_and_lots(driver)
        click_price(driver, price_low, price_high)
        parse(driver, good_listings, page_number, price_low, price_high, size_low, size_high, filename)


if __name__ == "__main__":
    main()
