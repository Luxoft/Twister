
import os, sys
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

sys.path.append(r'D:\TSC-Repository\Twister\Sources\Python')
sys.path.append(r'd:\Projects\twister\Sources\Python')
from libraries.ExposedLibraries import logMsg
logMsg('logDebug', 'Am inceput selenium!')

#

browser = webdriver.Firefox() # Get local session of firefox
browser.get('http://www.yahoo.com') # Load page
assert 'Yahoo!' in browser.title
elem = browser.find_element_by_name("p") # Find the query box
elem.send_keys('seleniumhq' + Keys.RETURN)
time.sleep(0.2) # Let the page load, will be added to the API
try:
    browser.find_element_by_xpath("//a[contains(@href,'http://seleniumhq.org')]")
except NoSuchElementException:
    assert 0, "Can't find seleniumhq!"
browser.close()

#

logMsg('logDebug', 'Am terminat selenium!')
exit(0)
