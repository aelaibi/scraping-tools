import requests
import selenium
from selenium import webdriver

import codecs
import time

try:
    from urlparse import urljoin
    from urllib import urlretrieve
except ImportError:
    from urllib.parse import urljoin
    from urllib.request import urlretrieve



# HOST
HOST = 'http://hospitals.webometrics.info/en/world?page=%d'

SEP = ','
lineXPath = "//tr[contains(@class, 'odd')]|//tr[contains(@class, 'even')]"

_driver = webdriver.Firefox(executable_path='/Users/vpro/dev/projects/upwork/datascraping/geckodriver')

HEAD = 'Hospital Name, Country, URL'


print 'browser open'
_driver.maximize_window()



hospital_items = []


def scrapOnePage(page):
    _driver.get(urljoin(HOST %page, ""))
    print 'url loaded'
    print 'start scraping page ', page
    for ele in _driver.find_elements_by_xpath(lineXPath):
        link = ele.find_element_by_tag_name('a').get_attribute('href')
        country = ele.find_element_by_tag_name('img').get_attribute('src')
        items = ele.text.split('\n')
        rank = items[0]
        hname = items[1]
        hospital_items.append(hname + SEP + country[-6:][:2] + SEP + link)
        # print hname, SEP,  country[-6:][:2], SEP, link

for page in range(120):
    scrapOnePage(page)

with codecs.open('data.csv', 'w', encoding='utf-8') as fout:
    fout.write(HEAD)
    for line in hospital_items:
        fout.write(line + '\n')

time.sleep(2)

print 'end'

_driver.quit()