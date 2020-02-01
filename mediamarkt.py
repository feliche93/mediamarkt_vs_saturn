from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


driver = webdriver.Chrome(
    executable_path='/Users/felixvemmer/OneDrive/Dokumente/Hobbies/Programming/Python/chromedriver')
driver.get('https://www.mediamarkt.de')

# Einverstanden button
driver.find_element_by_xpath(
    '//button[@class="mms-button primary large"]').click()

driver.find_element_by_xpath(
    '//button[@class="mms-button-v2 mms-button-v2--size-s mms-button-v2--type-secondary categories-button"]').click()

categories = driver.find_elements_by_xpath(
    '//li[@class="category-list__element"]')

category_urls = []

counter = len(categories) + 1
e = 0

while e < counter:
    categories = driver.find_elements_by_xpath(
        '//li[@class="category-list__element"]')
    driver.implicitly_wait(10)
    categories[e].click()
    category_url = driver.current_url
    category_urls.append(category_url)
    driver.get('https://www.mediamarkt.de')
    driver.find_element_by_xpath(
        '//button[@class="mms-button-v2 mms-button-v2--size-s mms-button-v2--type-secondary categories-button"]').click()
    e += 1


class Mediamarkt():

    def __init__(self, executable_path, start_url):
        self.executable_path = executable_path
        self.driver = driver = webdriver.Chrome(
            executable_path=self.executable_path)
        self.start_url = start_url

    def get_category_links(self):
        self.driver.get(self.start_url)


mediamarkt = Mediamarkt(executable_path='/Users/felixvemmer/OneDrive/Dokumente/Hobbies/Programming/Python/chromedriver',
                        start_url='https://www.mediamarkt.de')

mediamarkt.get_category_links()
