from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import lxml

DRIVER_PATH = "C:\development\chromedriver-win64\chromedriver.exe"

parameters = {
    "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 "
                  "Safari/537.36",
}



class DataManager:
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_experimental_option("detach", value=True)
        self.service = Service(executable_path=DRIVER_PATH)
        self.driver = webdriver.Chrome(service=self.service, options=self.chrome_options)
        self.driver.get(
            "https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors#csr-gridpage-bottom"
        )
        self.driver.maximize_window()
        self.page_source = self.driver.page_source

        self.soup = BeautifulSoup(self.page_source, "lxml")
        self.majors = []
        self.early_career_pay = []
        self.mid_career_pay = []

        self.get_majors()
        self.get_early_career_pay()
        self.get_mid_career_pay()
        self.get_data_dictionary()

    def get_majors(self):
        majors = self.soup.find_all(name='td', class_='csr-col--school-name')

        for major in majors:
            major_name = major.find('span', class_='data-table__value').text
            self.majors.append(major_name)

    def get_early_career_pay(self):
        early_career_pay = self.soup.find_all(name='td', class_='csr-col--right')
        for element in early_career_pay:
            title_span = element.find('span', class_='data-table__title')
            if title_span and 'Early Career Pay' in title_span.text:
                value_span = element.find('span', class_='data-table__value')
                if value_span:
                    early_career_pay_value = value_span.text
                    self.early_career_pay.append(early_career_pay_value)
        return None

    def get_mid_career_pay(self):

        mid_career_pay = self.soup.find_all(name='td', class_='csr-col--right')
        for element in mid_career_pay:
            title_span = element.find('span', class_='data-table__title')
            if title_span and 'Mid-Career Pay' in title_span.text:
                value_span = element.find('span', class_='data-table__value')
                if value_span:
                    mid_career_pay_value = value_span.text
                    self.mid_career_pay.append(mid_career_pay_value)
        return None

    def get_data_dictionary(self):
        data = {
            "major": self.majors,
            "early_career_pay": self.early_career_pay,
            "mid_career_pay": self.mid_career_pay
        }
        print(data["major"][0])
        print(data["early_career_pay"][0])


DataManager()


