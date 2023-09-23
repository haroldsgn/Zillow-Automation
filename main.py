import time

from bs4 import BeautifulSoup
import lxml
import os
import re

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = os.environ.get("ZILLOW")
GOOGLE_FORM = "https://docs.google.com/forms/d/e/1FAIpQLSdD2I1zcKXN1knS9x0Q88WbmvldalBxrZbxu-sux-aHWK6hCA/viewform"
DRIVER_PATH = "C:\development\chromedriver-win64\chromedriver.exe"

parameters = {
    "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 "
                  "Safari/537.36",
}


class Datamanager:

    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_experimental_option("detach", True)
        self.service = Service(executable_path=DRIVER_PATH)
        self.driver = webdriver.Chrome(service=self.service, options=self.chrome_options)
        self.driver.get(URL)
        self.driver.maximize_window()
        self.page_source = self.driver.page_source

        self.soup = BeautifulSoup(self.page_source, "lxml")
        self.all_addresses = []
        self.all_prices = []
        self.all_links = []

        self.get_links()
        self.get_prices()
        self.get_addresses()
        self.google_sheets()

    def get_links(self):

        links = self.soup.find_all(name='a', class_="property-card-link")

        for link in links:
            href = link.get("href")
            if href and ("/apartments/" in href or "/b" in href):
                if not href.startswith("https://www.zillow.com"):
                    href = "https://www.zillow.com" + href
                self.all_links.append(href)

    def get_prices(self):

        cleaning_prices_list = []
        prices = self.soup.select('span[data-test="property-card-price"]')

        for price in prices:
            prices_list = price.getText().split()[0]
            cleaning_prices_list.append(prices_list)

        for data_price in cleaning_prices_list:
            clean_price = int(''.join(re.findall(r'\d+', data_price)))
            self.all_prices.append(clean_price)

    def get_addresses(self):

        addresses = self.soup.select('address[data-test="property-card-addr"]')

        for address in addresses:
            self.all_addresses.append(address.text)

    def google_sheets(self):

        self.driver.get(GOOGLE_FORM)
        wait = WebDriverWait(self.driver, 1)

        for n in range(len(self.all_prices)):
            address = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div['
                                                                           '1]/div/div/div['
                                                                           '2]/div/div[1]/div/div[1]/input')))
            price = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div['
                                                                         '2]/div/div/div['
                                                                         '2]/div/div[1]/div/div[1]/input')))
            link = wait.until(EC.presence_of_element_located((By.XPATH,
                                                              '//*[@id="mG61Hd"]/div[2]/div/div[2]/div['
                                                              '3]/div/div/div[2]/div/div['
                                                              '1]/div/div[1]/input')))
            submit_info = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div['
                                                                               '3]/div[1]/div[1]/div')))

            address.send_keys(self.all_addresses[n])
            price.send_keys(self.all_prices[n])
            link.send_keys(self.all_links[n])

            submit_info.click()

            send_another_response = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div['
                                                                                     '2]/div[1]/div/div[4]/a')))
            send_another_response.click()


Datamanager()
