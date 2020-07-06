from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


class LandListing:
    def __init__(self, price=0, link='', size=0, address=0):
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


def parse_listing_link(listing):
    return listing.find_element_by_class_name("list-card-info").find_element_by_tag_name("a").get_attribute("href")


def parse_listing(listing):
    price = parse_listing_price(listing)
    address = parse_listing_address(listing)
    listing_type = parse_listing_type(listing)
    link = parse_listing_link(listing)
    return [price, address, listing_type, link]


def output_list(list):
    for item in list:
        print(item)


def main():
    # price = float(input("Enter price limit: "))
    # size = float(input("Enter number of acres: "))

    good_listings = []

    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    global driver
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.get("https://zillow.com/homes/celina_rb/")

    html_data = driver.page_source
    listings = driver.find_elements_by_class_name("list-card")

    print("Number of listings on this page: " + str(len(listings)))

    for listing in listings:
        good_listings.append(parse_listing(listing))

    output_list(good_listings)


if __name__ == "__main__":
    main()

