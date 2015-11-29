# upload multiple files to garmin connect
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
import os
import time
import sys

# user dependent info
folder = r'C:\ProgramData\Garmin\CoreService\Devices\3841441873\Sync\FitnessHistory'
email = "Input your registered email address"
password = "Input your registered password"

# get file list
files = []
for file in os.listdir(folder):
    if file.lower().endswith(".tcx") or file.lower().endswith(".gpx"):
        files.append(file)


# functions to be used in waiting process
def ajax_complete(driver):
    try:
        return 0 == driver.execute_script("return jQuery.active")
    except WebDriverException:
        pass

def isCurrentUrlModern(driver):
    url = "https://connect.garmin.com/modern/"
    try:
        return url == driver.current_url
    except WebDriverException:
        pass

def isDisplayedElementByXPath(driver, xpath):
    try:
        element = driver.find_element_by_xpath(xpath)
        return element.is_displayed() 
    except:
        return False

# login -- start here
driver = webdriver.Firefox()
urlLogin="https://connect.garmin.com/signin"
urlActivities="https://connect.garmin.com/minactivities#"
driver.get(urlLogin)
WebDriverWait(driver, 20).until(
             ajax_complete,  "Timeout waiting for page to load")
actions = ActionChains(driver)
actions.send_keys(email)
actions.send_keys(Keys.TAB)
actions.send_keys(password)
actions.send_keys(Keys.ENTER)
actions.perform()

# show dashboard
WebDriverWait(driver, 20).until(
             isCurrentUrlModern,  "Timeout waiting for page to load")

# show Activities
driver.get(urlActivities)

for file in files:
# open Import popup
    WebDriverWait(driver, 20).until(
                 lambda driver: driver.find_element_by_link_text('Import'))
    linkImport = driver.find_element_by_link_text('Import')
    linkImport.click()


# show file upload dialogue
    uploadFormXPath = "//form[@id='uploadForm']"

    while isDisplayedElementByXPath(driver, uploadFormXPath) == False:
        linkImport.click()
        time.sleep(1)
        
    uploadFileSelect = driver.find_element_by_xpath("//form[@id='uploadForm']/input[@id='data']")

    time.sleep(2)

# filename input
    fullpath = folder + "\\" + file
    uploadFileSelect.send_keys(fullpath)

    uploadFromFileButton = driver.find_element_by_xpath("//form[@id='uploadForm']/input[@id='uploadFromFileButton']")
    uploadFromFileButton.click()
    time.sleep(1)
# upload
    closeButton = driver.find_element_by_xpath("//div[@id='overlay-manual-upload']/div[@class='overlay-header']/a[1]")
    closeButton.click()

#finish
