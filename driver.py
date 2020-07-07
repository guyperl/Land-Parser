from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import random


class LandListing:
    def __init__(self, price=0, link='', size='', address=0, listing_type=''):
        self.price = price
        self.link = link
        self.size = size
        self.address = address
        self.listing_type = listing_type

    def get_price(self):
        return self.price

    def get_link(self):
        return self.link

    def get_size(self):
        return self.size

    def get_address(self):
        return self.address

    def get_listing_type(self):
        return self.listing_type

    def set_price(self, price=0):
        self.price = price

    def set_link(self, link=''):
        self.link = link

    def set_size(self, size=0):
        self.size = size

    def set_address(self, address=''):
        self.address = address

    def set_listing_type(self, listing_type=''):
        self.listing_type = listing_type

    def price_in_range(self, low, high):
        return low <= self.price <= high

    def __str__(self):
        string = "Address: " + self.get_address() + "\n"
        string += "Size: " + self.get_size() + "\n"
        string += "Price: " + str(self.get_price()) + "\n"
        string += "Listing type: " + self.get_listing_type() + "\n"
        string += "Link: " + self.get_link() + "\n"
        return string


def turn_numeric(string):
    return_string = ''

    for i in range(len(string)):
        if string[i].isnumeric():
            return_string += string[i]

    return int(return_string)


def parse_listing_price(listing):
    price = listing.find_element_by_class_name("list-card-price").text
    price = turn_numeric(price)
    return price


def parse_listing_address(listing):
    return listing.find_element_by_class_name("list-card-addr").text


def parse_listing_type(listing):
    return listing.find_element_by_class_name("list-card-type").text


def parse_listing_size(listing):
    return listing.find_element_by_class_name("list-card-details").text


def parse_listing_link(listing):
    return listing.find_element_by_class_name("list-card-info").find_element_by_tag_name("a").get_attribute("href")


def parse_listing(listing):
    price = parse_listing_price(listing)
    address = parse_listing_address(listing)
    listing_type = parse_listing_type(listing)
    link = parse_listing_link(listing)
    size = parse_listing_size(listing)
    return LandListing(price=price, address=address, size=size, link=link, listing_type=listing_type)


def output_list(list):
    for item in list:
        print(item)


def main():
    # price = float(input("Enter price limit: "))
    # size = float(input("Enter number of acres: "))
    page_number = 1

    good_listings = []

    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    global driver
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.get("https://zillow.com/homes/celina_rb/")

    html_data = driver.page_source

    next_page_button = driver.find_element_by_class_name('cUjspl')
    next_page_link = next_page_button.get_attribute('href')

    while next_page_link:
        print('Parsing Page ' + str(page_number))
        listings = driver.find_elements_by_class_name("list-card")

        print("Number of listings on this page: " + str(len(listings)))

        for listing in listings:
            good_listings.append(parse_listing(listing))
            time.sleep(random.uniform(5, 10))

        output_list(good_listings)

        next_page_button = driver.find_element_by_class_name('cUjspl')
        next_page_link = next_page_button.get_attribute('href')

        driver.get(next_page_link)

        next_page_button = driver.find_element_by_class_name('cUjspl')
        next_page_link = next_page_button.get_attribute('href')

        time.sleep(random.uniform(20, 40))

        page_number += 1


if __name__ == "__main__":
    main()

