from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


def main():
    # price = float(input("Enter price limit: "))
    # size = float(input("Enter number of acres: "))

    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    global driver
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.get("https://zillow.com/homes/celina_rb/")

    html_data = driver.page_source

    print(html_data)

    # driver.quit()

if __name__ == "__main__":
    main()

